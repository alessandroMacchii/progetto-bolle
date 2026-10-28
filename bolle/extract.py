"""Estrazione dei dati da una pagina di bolla.

L'estrattore e' un'interfaccia con piu' implementazioni intercambiabili
(variabile `BOLLE_EXTRACTOR` in .env):

  claude  produzione. Un modello vision con structured output: regge i sei
          layout osservati e anche quelli che non abbiamo ancora visto.
  openrouter  stesso prompt e stesso schema, ma verso un modello di un altro
          fornitore (Gemini, GPT, Qwen...) via OpenRouter. Serve a confrontare.
          Chiave in OPENROUTER_API_KEY, modello in BOLLE_OPENROUTER_MODEL.
  consenso  due modelli economici via OpenRouter; se non concordano sul carico
          legge il modello forte. Costa ~la meta' di Opus da solo a parita' di
          qualita' sul banco di prova. Vedi `EstrattoreConsenso`.
  mock    nessuna chiamata di rete, rilegge il gold set. Serve a provare
          interfaccia ed export senza spendere e senza credenziali.

Il resto dell'applicazione conosce solo `estrai(jpg, numero) -> PaginaEstratta`,
quindi cambiare motore non tocca ne' l'interfaccia ne' l'export.
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Protocol

from .config import CONSENSO_ARBITRO, CONSENSO_MODELLI, MODEL, OPENROUTER_MODEL
from .ingest import come_base64
from .schema import PaginaEstratta

ISTRUZIONI = """Sei un assistente che digitalizza bolle di consegna cartacee scansionate.
Il fornitore e' sempre adidas, il destinatario sempre Jute Sport SRL.

Estrai SOLO quello che e' STAMPATO. Le scritte a mano non vanno mai usate per
correggere i dati stampati: vanno trascritte a parte (`annotazioni_manoscritte`,
`codice_manoscritto`, `correzioni`, `magazzini_per_taglia`, `magazzino_pagina`,
`note_pagina`) e sara' il programma ad applicarle, mostrando all'operatore il
valore stampato e quello corretto. Questa separazione e' la regola piu' importante: se sovrascrivi un dato
stampato con la tua lettura di una calligrafia, nessuno puo' piu' controllarla.

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
- Scritto accanto o sopra una riga: va su quella riga. Se la scritta copre i
  token Size/Qty di una riga, appartiene a QUELLA riga anche se sconfina nella
  riga sopra o sotto.
- Una graffa o una parentesi a margine che abbraccia piu' righe: va su OGNUNA
  delle righe abbracciate.
- Una sola scritta per tutta la pagina ("TUTTO MAG 2", un MAG grande in testa
  al foglio): mettila in `magazzino_pagina`, non sulle righe.
- Un magazzino non vale per forza per tutta la riga. Taglie diverse della
  stessa riga possono andare in magazzini diversi, e anche i pezzi di UNA
  STESSA taglia possono essere divisi fra piu' magazzini. Quando la scritta e'
  riferita a singole taglie o a singoli pezzi, trascrivila nelle annotazioni
  (es. "S: MAG 1; M, L: MAG 2" oppure "9-: 1 pezzo MAG 2, 2 pezzi MAG 1") e
  riportala in `magazzini_per_taglia`, una voce per ogni coppia taglia-magazzino,
  con la taglia STAMPATA come compare in `taglie`:
  {taglia_stampata: "M", magazzino: "MAG 2", qta: -1} se tutti i pezzi di quella
  taglia vanno li', qta: 2 se ce ne vanno solo 2. Esempio: sulla taglia stampata
  550 c'e' scritto "9-: 1 pezzo MAG 2, 2 pezzi MAG 1" -> due voci
  {taglia_stampata: "550", magazzino: "MAG 2", qta: 1} e
  {taglia_stampata: "550", magazzino: "MAG 1", qta: 2}.
  Non riassumere con un solo MAG per la riga e non inventare un magazzino per le
  taglie senza sigla: lasciale fuori. Se invece un solo MAG vale per tutta la
  riga, `magazzini_per_taglia` resta [].
- Su una riga barrata, o a cavallo fra una riga barrata e una attiva: un MAG
  NON barrato appartiene alla riga ATTIVA piu' vicina (di solito quella subito
  sotto), perche' a una riga cancellata non si assegna un magazzino. Resta sulla
  riga barrata solo un MAG barrato anche lui (cancellato insieme alla riga).
- Se la cifra non si distingue (1 oppure 2?) NON tirare a indovinare: scrivi
  "MAG ?" e spiega in `incertezze`.

ALTRE ANNOTAZIONI A MANO
- riga cancellata: metti `barrata` a true, ma estrai comunque tutti i dati
  stampati della riga. Conta come cancellata se c'e' ANCHE UNO SOLO di questi
  segni: un tratto di penna sopra il testo, uno scarabocchio sopra la riga, una
  X o una barra sul numero Seq-no. Guarda la colonna Seq-no riga per riga: una
  X piccola sul numero basta, anche se il resto della riga e' pulito.
- quantita' corrette a penna: lascia il valore STAMPATO nei campi dati, annota
  la correzione (es. "qta XS corretta a mano da 6 a 5") e riportala in
  `correzioni`: {taglia_stampata: "XS", taglia_corretta: "", qta_corretta: 5}.
- numeri scritti a mano sopra o sotto le taglie (es. "4-", "5", "6"): sono la
  taglia come la chiama il magazzino. Lascia la taglia STAMPATA nei campi dati,
  trascrivili nelle annotazioni e riportali in `correzioni`, una voce per ogni
  taglia stampata: {taglia_stampata: "550", taglia_corretta: "4-", qta_corretta: -1}.
  Abbina ogni numero scritto a mano alla taglia stampata che gli sta sopra o
  sotto, nell'ordine in cui compaiono.
- in `correzioni` usa -1 per una quantita' non corretta e "" per una taglia non
  corretta; se la stessa taglia ha corretti sia taglia sia quantita', una voce sola.
  Metti una correzione SOLO se leggi la scritta con sicurezza: se una cifra a
  mano e' ambigua non riportarla in `correzioni`, trascrivila nelle annotazioni
  e spiega in `incertezze`.
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
l'operatore smette di guardare. In particolare NON segnalare:
- quantita' coperte ma confermate dal Total di riga (il programma lo verifica
  gia' da solo);
- campi che non vanno nel carico: descrizione, colore, Seq-no, prezzo.
Segnala invece sempre codice articolo e NOMI di taglia letti a fatica: il Total
di riga non li controlla (550/2 e 580/2 danno lo stesso totale).

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
        # Come fa da se' l'SDK Anthropic: ritenta sui guasti passeggeri (troppe
        # richieste, provider sovraccarico, rete), non sugli errori nostri.
        for tentativo in range(3):
            try:
                with urllib.request.urlopen(richiesta, timeout=600) as r:
                    risposta = json.loads(r.read())
                break
            except urllib.error.HTTPError as exc:
                dettaglio = exc.read().decode("utf-8", "replace")[:400]
                if exc.code not in (408, 429, 500, 502, 503, 504) or tentativo == 2:
                    raise RuntimeError(f"OpenRouter HTTP {exc.code}: {dettaglio}") from exc
            except (urllib.error.URLError, TimeoutError) as exc:
                if tentativo == 2:
                    raise RuntimeError(f"OpenRouter non raggiungibile: {exc}") from exc
            time.sleep(2 * 4**tentativo)
        if "error" in risposta:
            raise RuntimeError(f"OpenRouter: {str(risposta['error'])[:400]}")
        testo = risposta["choices"][0]["message"].get("content") or ""
        # alcuni modelli incorniciano comunque il JSON in un blocco ```json
        testo = testo.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
        return PaginaEstratta.model_validate_json(testo)


# "MAG 1", "mag2", ma anche "M1" / "M. 2": come le scrive a margine il magazzino
_MAG = re.compile(r"(?<![A-Za-z0-9])M(?:AG)?\.?\s*(\d)(?![0-9])", re.IGNORECASE)


def _firma(pagina: PaginaEstratta) -> list[tuple]:
    """Quello che finisce nel carico, riga per riga: codice, taglie, barrata,
    magazzino (anche per taglia) e le correzioni a mano (codice e taglie) che il
    programma applica.

    Descrizioni, colori e note possono differire fra due modelli senza che il
    carico cambi; questi campi no.
    """
    firma = []
    for riga in pagina.righe:
        coppie = []
        for token in riga.size_qty_raw.split():
            taglia, _, qta = token.rpartition("/")
            if not taglia or not qta.isdigit():
                coppie = [(t.taglia.strip().upper(), t.qta) for t in riga.taglie]
                break
            coppie.append((taglia.upper(), int(qta)))
        magazzini = set(_MAG.findall(riga.annotazioni_manoscritte))
        if not magazzini and not riga.barrata:
            magazzini = set(_MAG.findall(pagina.magazzino_pagina))
        # le correzioni a mano entrano nel carico: due letture che le leggono
        # diverse non sono concordi
        correzioni = sorted(
            (c.taglia_stampata.strip().upper(), c.taglia_corretta.strip().upper(), c.qta_corretta)
            for c in riga.correzioni
        )
        # cosi' come le taglie divise fra magazzini
        per_taglia = sorted(
            (m.taglia_stampata.strip().upper(), tuple(_MAG.findall(m.magazzino)), m.qta)
            for m in riga.magazzini_per_taglia
        )
        firma.append(
            (
                riga.codice_articolo.strip().upper(),
                tuple(sorted(coppie)),
                riga.barrata,
                tuple(sorted(magazzini)),
                riga.codice_manoscritto.strip().upper(),
                tuple(correzioni),
                tuple(per_taglia),
            )
        )
    return firma


class EstrattoreConsenso:
    """Due modelli economici in parallelo; se non concordano decide il modello forte.

    Due modelli diversi raramente sbagliano allo stesso modo: il disaccordo
    intercetta anche gli errori che il singolo modello non sa di fare, cosa che
    l'auto-segnalazione (`incertezze`) non fa. Sul banco di prova, prompt v3,
    con Gemini 3.8 Flash + Haiku 5.5 e Opus 5.5 come arbitro: 36/37 pagine
    perfette (Opus da solo 35/37), 0 errori non segnalati, 0,033 $ a pagina
    invece di 0,070, con 9 pagine su 37 passate all'arbitro.
    """

    def __init__(
        self, modelli: list[str] = CONSENSO_MODELLI, arbitro: str = CONSENSO_ARBITRO
    ) -> None:
        if len(modelli) != 2:
            raise RuntimeError("BOLLE_CONSENSO_MODELLI deve elencare esattamente due modelli")
        self._lettori = [EstrattoreOpenRouter(m) for m in modelli]
        self._arbitro = EstrattoreOpenRouter(arbitro)
        self._nomi = [m.split("/")[-1] for m in modelli]
        self._nome_arbitro = arbitro.split("/")[-1]

    def estrai(self, jpg: Path, numero: int) -> PaginaEstratta:
        def leggi(lettore: EstrattoreOpenRouter) -> PaginaEstratta | Exception:
            try:
                return lettore.estrai(jpg, numero)
            except Exception as exc:
                return exc

        with ThreadPoolExecutor(max_workers=2) as pool:
            prima, seconda = pool.map(leggi, self._lettori)

        if isinstance(prima, Exception) or isinstance(seconda, Exception):
            motivo = "una lettura e' fallita"
        elif _firma(prima) == _firma(seconda):
            prima._motore = f"{self._nomi[0]} + {self._nomi[1]} concordi"
            return prima
        else:
            motivo = "letture discordi"

        pagina = self._arbitro.estrai(jpg, numero)
        pagina._motore = f"{self._nome_arbitro} ({motivo})"
        return pagina


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


def crea_estrattore(backend: str | None = None) -> Estrattore:
    from .config import EXTRACTOR_BACKEND

    scelta = (backend or EXTRACTOR_BACKEND).lower()
    if scelta == "claude":
        return EstrattoreClaude()
    if scelta == "openrouter":
        return EstrattoreOpenRouter()
    if scelta == "consenso":
        return EstrattoreConsenso()
    if scelta == "mock":
        return EstrattoreMock()
    raise ValueError(f"backend di estrazione sconosciuto: {scelta!r}")
