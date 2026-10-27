"""Estrazione dei dati da una pagina di bolla.

L'estrattore e' un'interfaccia con piu' implementazioni intercambiabili
(variabile `BOLLE_EXTRACTOR` in .env):

  claude  produzione. Un modello vision con structured output: regge i sei
          layout osservati e anche quelli che non abbiamo ancora visto.
  openrouter  stesso prompt e stesso schema, ma verso un modello di un altro
          fornitore (Gemini, GPT, Qwen...) via OpenRouter. Serve a confrontare.
          Chiave in OPENROUTER_API_KEY, modello in BOLLE_OPENROUTER_MODEL.
  mock    nessuna chiamata di rete, rilegge il gold set. Serve a provare
          interfaccia ed export senza spendere e senza credenziali.
  local   segnaposto per un motore OCR in casa (Tesseract/PaddleOCR, oppure un
          VLM su GPU). Non implementato: vedi README, "Portare tutto in casa".

Il resto dell'applicazione conosce solo `estrai(jpg, numero) -> PaginaEstratta`,
quindi cambiare motore non tocca ne' l'interfaccia ne' l'export.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol

from .config import MODEL, OPENROUTER_MODEL
from .ingest import come_base64
from .schema import PaginaEstratta

ISTRUZIONI = """Sei un assistente che digitalizza bolle di consegna cartacee scansionate.
Il fornitore e' sempre adidas, il destinatario sempre Jute Sport SRL.

Estrai SOLO quello che e' STAMPATO. Le scritte a mano non vanno mai usate per
correggere i dati stampati: vanno trascritte a parte (`annotazioni_manoscritte`,
`codice_manoscritto`, `magazzino_pagina`, `note_pagina`) e sara' un operatore a
decidere. Questa separazione e' la regola piu' importante: un dato stampato che
sostituisci con la tua lettura di una calligrafia diventa un errore che finisce
dritto in magazzino.

LAYOUT CHE PUOI INCONTRARE (ne esistono altri: adattati)
1. DELIVERY NOTE con colonne Seq-no | Article | Name | Total | Size/Qty | Price
   e un riquadro SUMMARY con Total Pieces / Total Cartons.
2. Variante compatta dello stesso: piu' articoli sotto un unico blocco
   "Order From", con Total Pieces / Total Cartons in coda alla colonna Name.
   Ogni Seq-no e' una riga distinta, anche se condivide il blocco d'ordine.
3. Variante a spaziatura fissa (stampa ad aghi), stesse colonne.
4. CONSOLIDATED ORDER NUMBER: come sopra, intestazione diversa.
5. Delivery Note "Value Added Service": colonne Item No | Article No |
   Description | Line quantity | Unit | Sizes/Quantities.
6. mi adidas Product Specification / TechDoc: niente tabella di righe. Il codice
   articolo e' il valore accanto all'etichetta "Article Number" (NON "Factory
   Code", NON "Working Number") e le quantita' stanno in una "Size Table"
   verticale con colonne Sourcing size | Size IT | Qty. Trattalo come UNA riga
   sola, usando la colonna "Size IT" come taglia, e ricostruisci `size_qty_raw`
   nel formato compatto (es. "XS/2 S/2 M/3").

Le pagine successive alla prima di una bolla lunga non hanno intestazione ne'
SUMMARY: metti `continua_da_pagina_precedente` a true e 0 nel Total Pieces.

COLONNA Size/Qty
E' una sequenza di token `TAGLIA/QUANTITA`. La taglia va copiata ESATTAMENTE
come stampata, senza interpretarla; la quantita' e' il numero dopo l'ULTIMA
barra del token:
  8-/2                 mezza taglia calzatura, il trattino fa parte della taglia
  9-/3 11-/1           piu' taglie sulla stessa riga
  XS/2 S/7 M/10 L/8    abbigliamento
  XS/183 XL/50         quantita' a tre cifre
  NS/5  OSFM/10        taglia unica
  5/20                 taglia "5", quantita' 20
  5-6A/1 7-8A/6 910A/5 1112/5 1314/5   taglie bambino
  540/3 560/6          codici numerici calzatura (vanno di 10 in 10: 510 ... 640)
  3XLT/1 ST2/1 LT2/1 2XT2/1 2XL/4      taglie speciali
  XS/L/1 S/XL/2        pacco misto: piu' taglie nello stesso pacco. In `taglie`
                       riporta il token cosi' com'e' (taglia "S/XL", quantita' 2):
                       la scomposizione in S e XL la fa il programma. Nel Total
                       di riga ogni pacco conta una volta sola
Quando i token sono impaginati su piu' colonne e piu' righe leggili tutti: e'
facile saltarne uno. Il campo `Total` di riga deve corrispondere alla somma
delle quantita': se non torna, ricontrolla la lettura prima di rispondere.

RIGHE
Riporta TUTTE le righe della tabella, anche su pagine fitte, ruotate o di
cattiva qualita'. Prima di rispondere controlla che i Seq-no siano consecutivi:
un buco vuol dire che hai saltato una riga.

MAGAZZINI SCRITTI A MANO
I magazzini sono "MAG 1" e "MAG 2", a penna o a matita, a volte evidenziati o
cerchiati, a volte abbreviati ("M1", "M 2", "mag2"). In `annotazioni_manoscritte`
scrivili sempre nella forma normalizzata "MAG 1" / "MAG 2".
- Scritto accanto o sopra una riga: va su quella riga.
- Una graffa o una parentesi a margine che abbraccia piu' righe: va su OGNUNA
  delle righe abbracciate.
- Una sola scritta per tutta la pagina ("TUTTO MAG 2", un MAG grande in testa
  al foglio): mettila in `magazzino_pagina`, non sulle righe.
- Riferito a singole taglie: scrivi a quali, es.
  "9-: 1 pezzo MAG 2, 2 pezzi MAG 1".
- A cavallo fra una riga barrata e una riga attiva: appartiene alla riga
  ATTIVA, perche' a una riga cancellata non si assegna un magazzino. Se invece
  sta chiaramente sulla riga barrata, o e' barrato anche lui, lascialo li'.
- Se la cifra non si distingue (1 oppure 2?) NON tirare a indovinare: scrivi
  "MAG ?" e spiega in `incertezze`.

ALTRE ANNOTAZIONI A MANO
- riga cancellata con un tratto di penna, uno scarabocchio o una X (anche solo
  sul numero di riga): metti `barrata` a true, ma estrai comunque tutti i dati
  stampati della riga.
- quantita' o taglie corrette a penna: lascia il valore STAMPATO nei campi dati e
  annota la correzione, es. "qta XS corretta a mano da 6 a 5".
- numeri scritti a mano sopra o sotto le taglie (es. "4-", "5", "6"): sono la
  taglia come la chiama il magazzino. Trascrivili nelle annotazioni; NON
  sostituiscono la taglia stampata.
- codice articolo scritto a mano: va in `codice_manoscritto` della riga a cui si
  riferisce, MAI in `codice_articolo`, nemmeno se quello stampato e' piccolo o
  difficile da leggere. Non inventare una riga per un codice scritto a mano.
- nomi di clienti o squadre (es. "VERONELLI"): nelle annotazioni della riga.
- spunte, "ok", conteggi di colli, firme: in `note_pagina`. Non sono magazzini.

QUANDO NON SEI SICURO
Le scritte a penna a volte coprono lo stampato. Leggi sotto se ci riesci. Per
ogni dato stampato che hai letto a fatica (una lettera del codice coperta, una
cifra della taglia sotto una X, un carattere minuscolo) scrivi in `incertezze`
quale campo e quali sono le letture possibili, es. "taglia: 550 oppure 580,
cifra centrale coperta". Metti comunque nel campo la lettura piu' probabile.
Se un numero scritto a mano accanto a una taglia aiuta a capire quale delle due
letture e' giusta puoi tenerne conto, ma dillo in `incertezze`.
Lascia `incertezze` vuoto quando la lettura e' netta: se segnali tutto,
l'operatore smette di guardare.

ALTRE REGOLE
- Se un valore non e' leggibile affatto usa "" per le stringhe e 0 per i numeri.
  Non inventare mai un codice articolo.
- `rotazione_gradi`: di quanto va ruotata l'immagine in senso orario per
  raddrizzarla (0, 90, 180, 270)."""


class Estrattore(Protocol):
    def estrai(self, jpg: Path, numero: int) -> PaginaEstratta: ...


class EstrattoreClaude:
    """Backend di produzione: modello vision + structured output."""

    def __init__(self, model: str = MODEL) -> None:
        import os

        import anthropic

        # Il client non verifica le credenziali finche' non parte una chiamata:
        # senza questo controllo l'errore arriverebbe a meta' caricamento, una
        # volta per pagina, e con un messaggio incomprensibile.
        if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")):
            raise RuntimeError(
                "Manca ANTHROPIC_API_KEY: copia .env.example in .env e inserisci "
                "la chiave. Per provare l'applicazione senza chiave usa "
                "BOLLE_EXTRACTOR=mock."
            )
        self._client = anthropic.Anthropic()
        self._model = model

    def estrai(self, jpg: Path, numero: int) -> PaginaEstratta:
        risposta = self._client.messages.parse(
            model=self._model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=ISTRUZIONI,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": come_base64(jpg),
                            },
                        },
                        {
                            "type": "text",
                            "text": "Estrai i dati di questa pagina "
                            f"(pagina {numero} del documento caricato).",
                        },
                    ],
                }
            ],
            output_format=PaginaEstratta,
        )
        if risposta.stop_reason == "refusal":
            raise RuntimeError(
                "Il modello ha rifiutato di elaborare la pagina; "
                "inserisci le righe manualmente."
            )
        return risposta.parsed_output


def schema_stretto() -> dict:
    """Lo schema con `additionalProperties: false`, richiesto dagli output vincolati."""
    schema = PaginaEstratta.model_json_schema()

    def chiudi(nodo):
        if isinstance(nodo, dict):
            if nodo.get("type") == "object":
                nodo["additionalProperties"] = False
                nodo["required"] = list(nodo.get("properties", {}))
            for figlio in nodo.values():
                chiudi(figlio)
        elif isinstance(nodo, list):
            for figlio in nodo:
                chiudi(figlio)

    chiudi(schema)
    return schema


class EstrattoreOpenRouter:
    """Modelli di altri fornitori (Gemini, GPT, ...) con lo stesso prompt e schema."""

    URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, model: str = OPENROUTER_MODEL) -> None:
        self._chiave = os.getenv("OPENROUTER_API_KEY", "").strip()
        if not self._chiave:
            raise RuntimeError(
                "Manca OPENROUTER_API_KEY: inseriscila in .env "
                "(https://openrouter.ai/keys). Per provare senza chiave usa "
                "BOLLE_EXTRACTOR=mock."
            )
        self._model = model

    def estrai(self, jpg: Path, numero: int) -> PaginaEstratta:
        corpo = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": ISTRUZIONI},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{come_base64(jpg)}"},
                        },
                        {
                            "type": "text",
                            "text": "Estrai i dati di questa pagina "
                            f"(pagina {numero} del documento caricato).",
                        },
                    ],
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "pagina", "strict": True, "schema": schema_stretto()},
            },
            # senza questo OpenRouter puo' girare la richiesta a un provider
            # che ignora lo schema e risponde in testo libero
            "provider": {"require_parameters": True},
        }
        richiesta = urllib.request.Request(
            self.URL,
            data=json.dumps(corpo).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._chiave}",
                "X-Title": "Carico merci bolle",
            },
        )
        try:
            with urllib.request.urlopen(richiesta, timeout=600) as r:
                risposta = json.loads(r.read())
        except urllib.error.HTTPError as exc:
            dettaglio = exc.read().decode("utf-8", "replace")[:400]
            raise RuntimeError(f"OpenRouter HTTP {exc.code}: {dettaglio}") from exc
        if "error" in risposta:
            raise RuntimeError(f"OpenRouter: {str(risposta['error'])[:400]}")
        testo = risposta["choices"][0]["message"].get("content") or ""
        # alcuni modelli incorniciano comunque il JSON in un blocco ```json
        testo = testo.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
        return PaginaEstratta.model_validate_json(testo)


class EstrattoreMock:
    """Rilegge il gold set: prova l'app senza rete, credenziali o costi."""

    def __init__(self, gold: Path | None = None) -> None:
        gold = gold or Path(__file__).resolve().parent.parent / "gold" / "gold.json"
        self._dati = {
            int(k): v for k, v in json.loads(gold.read_text(encoding="utf-8")).items()
        }

    def estrai(self, jpg: Path, numero: int) -> PaginaEstratta:
        if numero not in self._dati:
            return PaginaEstratta(
                tipo_documento="ALTRO",
                numero_documento="",
                data_documento="",
                warehouse="",
                total_pieces_dichiarato=0,
                rotazione_gradi=0,
                continua_da_pagina_precedente=False,
                righe=[],
            )
        return PaginaEstratta.model_validate(self._dati[numero])


class EstrattoreLocale:
    """Segnaposto per un motore OCR in casa. Vedi README."""

    def estrai(self, jpg: Path, numero: int) -> PaginaEstratta:
        raise NotImplementedError(
            "Backend locale non implementato. Richiede Tesseract/PaddleOCR con "
            "regole per layout, oppure un VLM su GPU. Vedi README, sezione "
            "'Portare tutto in casa'."
        )


def crea_estrattore(backend: str | None = None) -> Estrattore:
    from .config import EXTRACTOR_BACKEND

    scelta = (backend or EXTRACTOR_BACKEND).lower()
    if scelta == "claude":
        return EstrattoreClaude()
    if scelta == "openrouter":
        return EstrattoreOpenRouter()
    if scelta == "mock":
        return EstrattoreMock()
    if scelta == "local":
        return EstrattoreLocale()
    raise ValueError(f"backend di estrazione sconosciuto: {scelta!r}")
