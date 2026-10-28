"""Server locale del prototipo.

Entry point: `python -m bolle.app` oppure `uvicorn bolle.app:api --reload`.
Orchestra ingest -> extract -> lavoro -> store -> excel.
"""
from __future__ import annotations

import base64
import hashlib
import os
import re
import secrets
import shutil
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any
from urllib.parse import unquote

from fastapi import FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, TypeAdapter, ValidationError

from . import excel, ingest, scan, store
from .config import (
    ACCESSO_PASSWORD,
    ACCESSO_UTENTE,
    ESTRAZIONI_PARALLELE,
    EXCEL_HEADERS,
    EXTRACTOR_BACKEND,
    IP_HEADER,
    MAGAZZINI,
    MAX_PAGINE,
    MAX_UPLOAD_MB,
    PAGES_DIR,
    UPLOAD_DIR,
)
from .extract import crea_estrattore
from .lavoro import costruisci_righe, riga_vuota, verifica_pagina
from .sizes import aggiungi_alla_mappa, normalizza_variante, uniforma_taglia

STATIC = Path(__file__).parent / "static"

# niente /docs ne' /openapi.json: online non serve descrivere l'API a nessuno
api = FastAPI(title="Bolle - carico merci", version="0.1.0", docs_url=None, redoc_url=None, openapi_url=None)


# --- accesso e sicurezza -------------------------------------------------------

# Tentativi di login sbagliati per indirizzo: dopo MAX_ERRORI in FINESTRA secondi
# l'indirizzo resta bloccato per BLOCCO secondi. Senza, la password si puo'
# provare a raffica.
MAX_ERRORI, FINESTRA, BLOCCO = 10, 300, 900
_errori_login: dict[str, list[float]] = {}
_bloccati: dict[str, float] = {}
_LUCCHETTO_LOGIN = threading.Lock()

# Header aggiunti a ogni risposta. La pagina ha script e stili in linea, da
# qui 'unsafe-inline'; tutto il resto, carattere compreso, viene dall'app.
# Script esterni e iframe sono chiusi.
_INTESTAZIONI_SICUREZZA = {
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data: blob:; "
        "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    ),
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Strict-Transport-Security": "max-age=31536000",
    "Cache-Control": "no-store",
}

_ID_DOCUMENTO = re.compile(r"^[0-9a-f]{12}$")


def _indirizzo(request: Request) -> str:
    """Chi sta chiamando, per il blocco dei tentativi.

    Dietro un proxy tutte le richieste arrivano dal proxy: l'indirizzo vero sta
    in un header (CF-Connecting-IP per il tunnel Cloudflare). Si legge SOLO se
    BOLLE_IP_HEADER lo dice: senza proxy davanti, quell'header lo scrive chi
    attacca, e cambiandolo a ogni tentativo aggirerebbe il blocco.
    """
    if IP_HEADER and request.headers.get(IP_HEADER):
        return request.headers[IP_HEADER]
    return request.client.host if request.client else "?"


def _credenziali_valide(intestazione: str) -> bool:
    utente, password = "", ""
    if intestazione.lower().startswith("basic "):
        try:
            utente, _, password = (
                base64.b64decode(intestazione[6:], validate=True).decode("utf-8").partition(":")
            )
        except ValueError:
            pass
    # confronto a tempo costante, e sempre entrambi: non si scopre quale dei
    # due e' sbagliato misurando i tempi di risposta
    ok_utente = secrets.compare_digest(utente.encode(), ACCESSO_UTENTE.encode())
    ok_password = secrets.compare_digest(password.encode(), ACCESSO_PASSWORD.encode())
    return ok_utente and ok_password


@api.middleware("http")
async def sicurezza(request: Request, call_next):
    """Login del browser (HTTP Basic) quando l'app e' online, piu' le difese di contorno.

    Sul PC dell'ufficio BOLLE_PASSWORD resta vuota e il login non c'e'. Online
    e' l'unica cosa fra internet, le bolle dei clienti e la chiave API.
    """
    risposta = await _controlla(request, call_next)
    for nome, valore in _INTESTAZIONI_SICUREZZA.items():
        risposta.headers.setdefault(nome, valore)
    return risposta


async def _controlla(request: Request, call_next):
    if ACCESSO_PASSWORD and request.url.path != "/salute":
        chi = _indirizzo(request)
        adesso = time.monotonic()
        with _LUCCHETTO_LOGIN:
            fino = _bloccati.get(chi, 0)
            if fino > adesso:
                return Response(
                    "Troppi tentativi sbagliati: riprova fra qualche minuto",
                    status_code=429,
                    headers={"Retry-After": str(int(fino - adesso) + 1)},
                )
        if not _credenziali_valide(request.headers.get("authorization", "")):
            # la prima richiesta del browser arriva sempre senza credenziali:
            # non e' un tentativo sbagliato, e' la domanda "serve il login?"
            if request.headers.get("authorization"):
                with _LUCCHETTO_LOGIN:
                    recenti = [x for x in _errori_login.get(chi, []) if adesso - x < FINESTRA]
                    recenti.append(adesso)
                    _errori_login[chi] = recenti
                    if len(recenti) >= MAX_ERRORI:
                        _bloccati[chi] = adesso + BLOCCO
                        _errori_login.pop(chi, None)
                        print(f"login: {chi} bloccato per {BLOCCO // 60} minuti", flush=True)
            return Response(
                "Accesso riservato",
                status_code=401,
                headers={"WWW-Authenticate": 'Basic realm="Carico merci", charset="UTF-8"'},
            )

    # Il browser rimanda da solo le credenziali Basic anche a richieste partite
    # da un altro sito (CSRF): chi modifica deve venire da questa stessa pagina.
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        if request.headers.get("sec-fetch-site", "same-origin") not in ("same-origin", "none"):
            return Response("Richiesta da un altro sito rifiutata", status_code=403)

    # gli id dei documenti finiscono nei percorsi su disco: solo il formato atteso
    parti = request.url.path.split("/")
    if len(parti) > 3 and parti[1:3] == ["api", "documenti"] and not _ID_DOCUMENTO.match(parti[3]):
        return Response("documento non trovato", status_code=404)

    return await call_next(request)


@api.get("/salute")
def salute() -> dict[str, str]:
    """Per il controllo di vita dell'hosting: niente password, niente dati."""
    return {"stato": "ok"}


# --- modelli di richiesta ----------------------------------------------------

# Testo corto per costruzione: un campo da 10 MB non e' una correzione, e
# finirebbe nel database e nell'Excel.
Testo = Annotated[str, Field(max_length=200)]


class ModificaRiga(BaseModel):
    codice_articolo: Testo | None = None
    descrizione: Testo | None = None
    colore: Testo | None = None
    taglia: Testo | None = None
    variante: Testo | None = None
    qta: Annotated[int, Field(ge=0, le=100_000)] | None = None
    magazzino: str | None = None
    eliminata: bool | None = None
    verificata: bool | None = None


class Divisione(BaseModel):
    qta: int
    magazzino: str


class NuovaVariante(BaseModel):
    taglia: Testo
    variante: Testo


class AssegnazioneMassiva(BaseModel):
    magazzino: str
    pagina: int | None = None


def _magazzino_valido(magazzino: str) -> None:
    if magazzino not in MAGAZZINI:
        raise HTTPException(400, f"magazzino sconosciuto: scegli fra {', '.join(MAGAZZINI)}")


# --- utilita' ----------------------------------------------------------------

def _doc(doc_id: str) -> dict[str, Any]:
    doc = store.carica(doc_id)
    if doc is None:
        raise HTTPException(404, "documento non trovato")
    return doc


def _salva(doc: dict[str, Any]) -> None:
    store.salva(doc["id"], {k: v for k, v in doc.items() if k not in store.COLONNE})


# --- chi fa cosa -------------------------------------------------------------
# L'operatore lo scrive l'interfaccia prima di caricare una bolla e lo manda con
# ogni richiesta nell'header X-Operatore (codificato: i nomi possono avere
# accenti, gli header no). Non e' un'autenticazione: il login resta uno per
# tutti. Serve a sapere, nell'Excel, chi ha caricato, corretto ed esportato.

MAX_OPERATORE = 60


def _operatore(request: Request) -> str:
    # l'export si scarica con un link, che non porta header: li' arriva in ?operatore=
    intestazione = request.headers.get("X-Operatore", "")
    grezzo = unquote(intestazione) if intestazione else request.query_params.get("operatore", "")
    nome = " ".join(grezzo.split())
    if not nome:
        raise HTTPException(400, "indica l'operatore prima di continuare")
    if len(nome) > MAX_OPERATORE:
        raise HTTPException(400, f"nome operatore troppo lungo: massimo {MAX_OPERATORE} caratteri")
    return nome


def _registra(
    doc: dict[str, Any],
    operatore: str,
    azione: str,
    riga: dict[str, Any] | None = None,
    campo: str = "",
    prima: Any = "",
    dopo: Any = "",
) -> None:
    """Una voce del registro delle modifiche: finisce nel foglio Modifiche."""
    riga = riga or {}
    doc.setdefault("storico", []).append(
        {
            "quando": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operatore": operatore,
            "azione": azione,
            "riga_id": riga.get("id", ""),
            "pagina": riga.get("pagina", ""),
            "seq": riga.get("seq", ""),
            "codice_articolo": riga.get("codice_articolo", ""),
            "taglia": riga.get("taglia", ""),
            "campo": campo,
            "prima": "" if prima is None else prima,
            "dopo": "" if dopo is None else dopo,
        }
    )


def _trova(doc: dict[str, Any], riga_id: str) -> dict[str, Any]:
    for r in doc["righe"]:
        if r["id"] == riga_id:
            return r
    raise HTTPException(404, "riga non trovata")


# --- API ---------------------------------------------------------------------

@api.get("/api/config")
def configurazione() -> dict[str, Any]:
    return {
        "magazzini": MAGAZZINI,
        "backend": EXTRACTOR_BACKEND,
        "colonne_export": EXCEL_HEADERS,
    }


@api.get("/api/documenti")
def lista_documenti() -> list[dict[str, Any]]:
    return store.elenca()


@api.get("/api/operatori")
def lista_operatori() -> list[str]:
    return store.operatori()


# Avanzamento delle letture in corso, {doc_id: [pagine lette, pagine totali]}.
# Vive in memoria: se il server si riavvia a meta' lettura, la bolla risulta
# interrotta e va ricaricata (vedi `stato_lettura`).
_IN_LETTURA: dict[str, list[int]] = {}
_LUCCHETTO = threading.Lock()


@api.post("/api/documenti")
def carica_documento(request: Request, file: UploadFile, forza: bool = False) -> dict[str, Any]:
    """Salva e rende le pagine, poi risponde subito: la lettura va in background.

    Una bolla da 14 pagine richiede minuti, e un proxy davanti al server (il
    tunnel della prova online, l'hosting dopo) chiude le richieste ferme da
    100 secondi. L'interfaccia chiede l'avanzamento a `/lettura`.

    Un file identico a uno gia' caricato si ferma con un 409 prima della
    lettura (che costa): l'interfaccia chiede se aprire quello esistente o
    rileggerlo, e in quel caso ripete la richiesta con `forza`.
    """
    operatore = _operatore(request)
    doc_id = store.nuovo_id()
    nome = Path(file.filename or "bolla").name[:120] or "bolla"
    if Path(nome).suffix.lower() not in ingest.FORMATI:
        raise HTTPException(400, "formato non supportato: carica un PDF o una foto")
    destinazione = UPLOAD_DIR / f"{doc_id}_{nome}"

    # copia a blocchi con un tetto: un file enorme riempirebbe il disco
    scritti = 0
    impronta = hashlib.sha256()
    with destinazione.open("wb") as fh:
        while blocco := file.file.read(1 << 20):
            scritti += len(blocco)
            if scritti > MAX_UPLOAD_MB << 20:
                fh.close()
                destinazione.unlink(missing_ok=True)
                raise HTTPException(413, f"file troppo grande: massimo {MAX_UPLOAD_MB} MB")
            impronta.update(blocco)
            fh.write(blocco)

    if not forza and (uguali := _stesso_file(impronta.hexdigest())):
        destinazione.unlink(missing_ok=True)
        raise HTTPException(
            409,
            {
                "messaggio": "questo file e' gia' stato caricato",
                "doppioni": [_in_breve(d) for d in uguali],
            },
        )

    try:
        pagine = ingest.carica(destinazione, doc_id, max_pagine=MAX_PAGINE)
    except ingest.TroppePagine as exc:
        destinazione.unlink(missing_ok=True)
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:  # file illeggibile: va detto, non ingoiato
        raise HTTPException(400, f"impossibile leggere il file: {type(exc).__name__}") from exc

    return _avvia_lettura(doc_id, nome, pagine, operatore, impronta.hexdigest())


def _impronta_di(doc: dict[str, Any]) -> str:
    """L'impronta salvata, o quella del file in uploads per le bolle caricate
    prima che la si salvasse."""
    if doc.get("impronta"):
        return doc["impronta"]
    for f in UPLOAD_DIR.glob(f"{doc['id']}_*"):
        if "_foto_p" not in f.name:
            return hashlib.sha256(f.read_bytes()).hexdigest()
    return ""


def _stesso_file(impronta: str) -> list[dict[str, Any]]:
    return [d for d in store.elenca() if _impronta_di(d) == impronta]


def _in_breve(doc: dict[str, Any]) -> dict[str, Any]:
    """Quanto basta per riconoscere una bolla gia' caricata."""
    return {k: doc.get(k, "") for k in ("id", "nome", "creato_il", "operatore", "esportato", "numeri")}


def _avvia_lettura(
    doc_id: str,
    nome: str,
    pagine: list[ingest.Pagina],
    operatore: str,
    impronta: str = "",
) -> dict[str, Any]:
    try:
        estrattore = crea_estrattore()
    except Exception as exc:  # tipicamente: credenziali mancanti
        raise HTTPException(503, str(exc)) from exc

    stato: dict[str, Any] = {
        "pagine": [], "righe": [], "in_lettura": True, "operatore": operatore, "storico": [],
        "impronta": impronta,
    }
    _registra(stato, operatore, "caricamento", dopo=nome)
    store.crea(doc_id, nome, stato)
    with _LUCCHETTO:
        _IN_LETTURA[doc_id] = [0, len(pagine)]
    threading.Thread(
        target=_leggi_documento, args=(doc_id, pagine, estrattore), daemon=True
    ).start()
    return {"id": doc_id, "nome": nome, "pagine_totali": len(pagine)}


def _leggi_documento(doc_id: str, pagine: list[ingest.Pagina], estrattore: Any) -> None:
    # Le pagine sono indipendenti: leggerle in parallelo porta una bolla da 14
    # pagine da ~6 minuti a ~1,5. L'ordine dei risultati resta quello del file.
    def leggi(pagina: ingest.Pagina) -> Any:
        try:
            return estrattore.estrai(pagina.jpg, pagina.numero)
        except Exception as exc:
            return exc
        finally:
            with _LUCCHETTO:
                _IN_LETTURA[doc_id][0] += 1

    try:
        with ThreadPoolExecutor(max_workers=ESTRAZIONI_PARALLELE) as pool:
            letture = list(pool.map(leggi, pagine))

        meta_pagine: list[dict[str, Any]] = []
        righe: list[dict[str, Any]] = []

        for pagina, estratta in zip(pagine, letture):
            voce: dict[str, Any] = {
                "numero": pagina.numero,
                "rotazione": pagina.rotazione_suggerita,
                "avvisi": [],
                "errore": "",
            }
            if isinstance(estratta, Exception):
                voce["errore"] = f"{type(estratta).__name__}: {estratta}"
                voce["avvisi"] = ["estrazione fallita: inserisci le righe a mano"]
                traceback.print_exception(estratta)
                meta_pagine.append(voce)
                continue

            righe_pagina = costruisci_righe(estratta, pagina.numero)
            voce.update(
                {
                    "tipo_documento": estratta.tipo_documento,
                    "numero_documento": estratta.numero_documento,
                    "data_documento": estratta.data_documento,
                    "warehouse": estratta.warehouse,
                    "total_pieces": estratta.total_pieces_dichiarato,
                    "avvisi": verifica_pagina(estratta, righe_pagina),
                    "motore": estratta._motore,
                }
            )
            # il modello vede la pagina meglio di un'euristica sui pixel
            if estratta.rotazione_gradi in (0, 90, 180, 270):
                voce["rotazione"] = estratta.rotazione_gradi
            meta_pagine.append(voce)
            righe.extend(r.model_dump() for r in righe_pagina)

        # chi ha caricato e il registro restano: si sostituiscono pagine e righe
        doc = store.carica(doc_id) or {}
        store.salva(
            doc_id,
            {
                "pagine": meta_pagine,
                "righe": righe,
                "operatore": doc.get("operatore", ""),
                "storico": doc.get("storico", []),
                "impronta": doc.get("impronta", ""),
            },
        )
    except Exception:
        traceback.print_exc()  # resta "in_lettura": stato_lettura la da' per interrotta
    finally:
        with _LUCCHETTO:
            _IN_LETTURA.pop(doc_id, None)


@api.get("/api/documenti/{doc_id}/lettura")
def stato_lettura(doc_id: str) -> dict[str, Any]:
    with _LUCCHETTO:
        avanzamento = _IN_LETTURA.get(doc_id)
        if avanzamento:
            return {"finita": False, "lette": avanzamento[0], "totali": avanzamento[1]}
    doc = _doc(doc_id)
    if doc.get("in_lettura"):
        return {"finita": True, "errore": "lettura interrotta (server riavviato?): ricarica il file"}
    return {"finita": True, "errore": ""}


@api.get("/api/documenti/{doc_id}")
def dettaglio(doc_id: str) -> dict[str, Any]:
    doc = _doc(doc_id)
    # stessa bolla caricata due volte (una foto e un PDF, o due scansioni):
    # il file e' diverso, il numero di documento no. Caricarla due volte nel
    # gestionale vorrebbe dire merce contata doppia.
    numeri = {p["numero_documento"] for p in doc.get("pagine", []) if p.get("numero_documento")}
    doc["doppioni"] = [
        {**_in_breve(d), "in_comune": sorted(numeri & set(d["numeri"]))}
        for d in store.elenca()
        if d["id"] != doc_id and numeri & set(d["numeri"])
    ]
    return doc


@api.get("/api/documenti/{doc_id}/pagine/{numero}.png")
def immagine(doc_id: str, numero: int) -> FileResponse:
    percorso = PAGES_DIR / doc_id / f"p{numero:03d}.png"
    if not percorso.exists():
        raise HTTPException(404, "pagina non trovata")
    return FileResponse(percorso, media_type="image/png")


@api.patch("/api/documenti/{doc_id}/righe/{riga_id}")
def modifica(
    request: Request, doc_id: str, riga_id: str, cambio: ModificaRiga
) -> dict[str, Any]:
    operatore = _operatore(request)
    if cambio.magazzino is not None:
        _magazzino_valido(cambio.magazzino)
    doc = _doc(doc_id)
    riga = _trova(doc, riga_id)
    for campo, valore in cambio.model_dump(exclude_none=True).items():
        if campo == "taglia":
            valore = uniforma_taglia(valore)
        if riga.get(campo) != valore:
            _registra(doc, operatore, "modifica", riga, campo, riga.get(campo), valore)
        riga[campo] = valore
        if campo == "taglia":
            # taglia nuova, variante nuova: la decide il CSV, come alla lettura,
            # e se non la conosce torna da validare
            variante, confermata = normalizza_variante(valore)
            riga["variante"], riga["variante_confermata"] = variante, confermata
            riga["avvisi"] = [
                a for a in riga.get("avvisi", []) if not a.startswith("variante '")
            ]
            if not confermata and valore:
                riga["avvisi"].append(
                    f"variante '{variante}' da confermare: la taglia '{valore}' "
                    "non e' in config/varianti.csv (confermandola ce la si aggiunge)"
                )
        if campo == "variante":
            riga["variante_confermata"] = True
            riga["avvisi"] = [
                a for a in riga.get("avvisi", []) if not a.startswith("variante '")
            ]
        if campo == "magazzino":
            # l'operatore ha deciso: anche i dubbi sul magazzino sono risolti
            riga["avvisi"] = [
                a for a in riga.get("avvisi", [])
                if "magazzino proposto" not in a
                and "piu' magazzini" not in a
                and "magazzino scritto a mano ma illeggibile" not in a
            ]
        if campo == "codice_articolo" and valore:
            riga["avvisi"] = [
                a for a in riga.get("avvisi", []) if "codice articolo non letto" not in a
            ]
    _salva(doc)
    return riga


@api.post("/api/documenti/{doc_id}/righe")
def aggiungi(request: Request, doc_id: str, pagina: int = 1) -> dict[str, Any]:
    operatore = _operatore(request)
    doc = _doc(doc_id)
    nuova = riga_vuota(pagina).model_dump()
    doc["righe"].append(nuova)
    _registra(doc, operatore, "riga aggiunta", nuova)
    _salva(doc)
    return nuova


@api.post("/api/documenti/{doc_id}/righe/{riga_id}/dividi")
def dividi(
    request: Request, doc_id: str, riga_id: str, divisione: Divisione
) -> dict[str, Any]:
    """Stessa taglia su due magazzini: il caso della pagina 3 degli esempi."""
    operatore = _operatore(request)
    _magazzino_valido(divisione.magazzino)
    doc = _doc(doc_id)
    riga = _trova(doc, riga_id)
    if divisione.qta < 1 or divisione.qta >= riga["qta"]:
        raise HTTPException(
            400, f"la quantita' da staccare deve stare fra 1 e {riga['qta'] - 1}"
        )

    puliti = [
        a
        for a in riga.get("avvisi", [])
        if "magazzino proposto" not in a and "piu' magazzini" not in a
    ]
    nuova = dict(riga)
    nuova["id"] = store.nuovo_id()
    nuova["qta"] = divisione.qta
    nuova["magazzino"] = divisione.magazzino
    nuova["origine"] = "split"
    nuova["avvisi"] = puliti
    _registra(doc, operatore, "divisione", riga, "qta", riga["qta"], riga["qta"] - divisione.qta)
    riga["qta"] -= divisione.qta
    riga["avvisi"] = puliti
    _registra(
        doc, operatore, "divisione", nuova, "magazzino",
        riga["magazzino"], f"{divisione.magazzino} (pezzi: {divisione.qta})",
    )

    doc["righe"].insert(doc["righe"].index(riga) + 1, nuova)
    _salva(doc)
    return {"originale": riga, "nuova": nuova}


@api.post("/api/documenti/{doc_id}/magazzino")
def assegna_massivo(
    request: Request, doc_id: str, richiesta: AssegnazioneMassiva
) -> dict[str, int]:
    operatore = _operatore(request)
    _magazzino_valido(richiesta.magazzino)
    doc = _doc(doc_id)
    toccate = 0
    for r in doc["righe"]:
        if r["eliminata"]:
            continue
        if richiesta.pagina is not None and r["pagina"] != richiesta.pagina:
            continue
        if r["magazzino"] != richiesta.magazzino:
            _registra(doc, operatore, "magazzino a piu' righe", r, "magazzino",
                      r["magazzino"], richiesta.magazzino)
        r["magazzino"] = richiesta.magazzino
        r["avvisi"] = [a for a in r.get("avvisi", []) if "magazzino proposto" not in a]
        toccate += 1
    _salva(doc)
    return {"righe_aggiornate": toccate}


@api.post("/api/documenti/{doc_id}/varianti")
def conferma_variante(
    request: Request, doc_id: str, richiesta: NuovaVariante
) -> dict[str, int]:
    """Taglia non in mappa confermata (o corretta) dall'operatore.

    Finisce nel CSV, cosi' le prossime bolle la trovano gia' tradotta, e vale
    subito per tutte le righe del documento con la stessa taglia ancora da
    confermare. Le righe gia' confermate a mano restano come sono.
    """
    operatore = _operatore(request)
    doc = _doc(doc_id)
    taglia = richiesta.taglia.strip().upper()
    variante = richiesta.variante.strip()
    try:
        aggiungi_alla_mappa(taglia, variante, f"confermata da {operatore} ({doc['nome']})")
    except ValueError as e:
        raise HTTPException(409, str(e)) from e
    toccate = 0
    for r in doc["righe"]:
        if r["variante_confermata"] or r["taglia"].strip().upper() != taglia:
            continue
        _registra(doc, operatore, "variante confermata", r, "variante", r["variante"], variante)
        r["variante"] = variante
        r["variante_confermata"] = True
        r["avvisi"] = [a for a in r.get("avvisi", []) if not a.startswith("variante '")]
        toccate += 1
    _salva(doc)
    return {"righe_aggiornate": toccate}


@api.get("/api/documenti/{doc_id}/verifica")
def verifica(doc_id: str) -> dict[str, Any]:
    doc = _doc(doc_id)
    return {
        "problemi": excel.problemi_bloccanti(doc["righe"]),
        "anteprima": [
            {"magazzino": m, "codice_articolo": c, "variante": v, "qta": q}
            for m, c, v, q in excel.aggrega(doc["righe"])
        ],
    }


@api.get("/api/documenti/{doc_id}/export")
def export(request: Request, doc_id: str) -> FileResponse:
    operatore = _operatore(request)
    doc = _doc(doc_id)
    problemi = excel.problemi_bloccanti(doc["righe"])
    if problemi:
        raise HTTPException(400, "; ".join(problemi))
    # registrato prima di scrivere il file, cosi' l'export compare nel suo Excel
    _registra(doc, operatore, "export")
    _salva(doc)
    percorso = excel.esporta(doc)
    store.segna_esportato(doc_id)
    return FileResponse(
        percorso,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=percorso.name,
    )


# --- scansione da fotocamera ---------------------------------------------------
# Senza stato: le foto restano nel browser finche' la bolla non e' completa, e
# ogni chiamata le rimanda. L'interfaccia le riduce a ~2600px prima, quindi
# pesano circa un mega l'una.

Punto = Annotated[list[Annotated[float, Field(ge=0, le=1)]], Field(min_length=2, max_length=2)]
Quadrilatero = Annotated[list[Punto], Field(min_length=4, max_length=4)]
_ANGOLI = TypeAdapter(Quadrilatero)
_SCANSIONE = TypeAdapter(list[tuple[Quadrilatero, bool]])

MAX_FOTO_MB = 15


def _byte_con_tetto(file: UploadFile, tetto_mb: int) -> bytes:
    dati = file.file.read((tetto_mb << 20) + 1)
    if len(dati) > tetto_mb << 20:
        raise HTTPException(413, f"foto troppo grande: massimo {tetto_mb} MB")
    return dati


def _foto(dati: bytes) -> Any:
    try:
        return scan.leggi(dati)
    except Exception as exc:
        raise HTTPException(400, f"immagine illeggibile: {type(exc).__name__}") from exc


def _elabora(img: Any, angoli: list[list[float]], pulisci: bool) -> Any:
    try:
        return scan.elabora(img, angoli, pulisci)
    except ValueError as exc:  # angoli degeneri: tutti nello stesso punto
        raise HTTPException(400, str(exc)) from exc


@api.post("/api/scan/bordi")
def scan_bordi(foto: UploadFile, veloce: bool = False) -> dict[str, Any]:
    """Dove sta il foglio nella foto. `veloce` salta i controlli di qualita':
    lo usa l'anteprima dal vivo, che chiede piu' volte al secondo."""
    img = _foto(_byte_con_tetto(foto, MAX_FOTO_MB))
    angoli = scan.trova_angoli(img)
    return {
        "angoli": angoli or scan.TUTTA_LA_FOTO,
        "trovati": angoli is not None,
        "avvisi": [] if veloce else scan.qualita(img, angoli),
    }


@api.post("/api/scan/anteprima")
def scan_anteprima(
    foto: UploadFile, angoli: Annotated[str, Form()], migliora: Annotated[bool, Form()] = True
) -> Response:
    try:
        quadrilatero = _ANGOLI.validate_json(angoli)
    except ValidationError as exc:
        raise HTTPException(400, "angoli non validi") from exc
    pagina = _elabora(_foto(_byte_con_tetto(foto, MAX_FOTO_MB)), quadrilatero, migliora)
    return Response(scan.jpeg(scan.riduci(pagina, 1400), 82), media_type="image/jpeg")


@api.post("/api/scan/documento")
def scan_documento(
    request: Request, foto: list[UploadFile], pagine: Annotated[str, Form()]
) -> dict[str, Any]:
    """Le foto della bolla, una per pagina, con i loro angoli: diventa un
    documento come uno caricato da file e va in lettura.

    `pagine` e' un JSON [[angoli, migliora], ...] nello stesso ordine delle foto.
    In uploads restano le foto originali (per rifare il ritaglio) e il PDF
    delle pagine elaborate, cioe' la scansione vera e propria.
    """
    operatore = _operatore(request)
    try:
        scelte = _SCANSIONE.validate_json(pagine)
    except ValidationError as exc:
        raise HTTPException(400, "angoli non validi") from exc
    if not foto or len(scelte) != len(foto):
        raise HTTPException(400, "serve una scelta di angoli per ogni foto")
    if len(foto) > MAX_PAGINE:
        raise HTTPException(400, f"troppe pagine: il massimo e' {MAX_PAGINE}")

    doc_id = store.nuovo_id()
    nome = time.strftime("scansione %d-%m-%Y %H.%M.pdf")
    elaborate = []
    for i, (file, (angoli, pulisci)) in enumerate(zip(foto, scelte), start=1):
        dati = _byte_con_tetto(file, MAX_FOTO_MB)
        img = _foto(dati)
        (UPLOAD_DIR / f"{doc_id}_foto_p{i:02d}.jpg").write_bytes(dati)
        elaborate.append(scan.in_pil(_elabora(img, angoli, pulisci)))

    elaborate[0].save(
        UPLOAD_DIR / f"{doc_id}_{nome}", "PDF", save_all=True,
        append_images=elaborate[1:], resolution=200, quality=85,
    )
    return _avvia_lettura(doc_id, nome, ingest.da_immagini(elaborate, doc_id), operatore)


# --- interfaccia -------------------------------------------------------------

api.mount("/static", StaticFiles(directory=STATIC), name="static")


@api.get("/", response_class=HTMLResponse)
def home() -> str:
    return (STATIC / "index.html").read_text(encoding="utf-8")


def main() -> None:
    import uvicorn

    # In locale ascolta solo sul PC; nel container BOLLE_HOST=0.0.0.0
    uvicorn.run(
        api,
        host=os.getenv("BOLLE_HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
    )


if __name__ == "__main__":
    main()
