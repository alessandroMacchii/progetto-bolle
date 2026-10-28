# CLAUDE.md

Prototipo per Jute Sport SRL: bolle di consegna adidas scansionate (PDF/foto) →
estrazione con modello vision → revisione dell'operatore in un'interfaccia web →
Excel per il carico massivo nel gestionale (Magazzino, Codice Articolo, Variante,
Quantita). Il README e' la documentazione completa: scelte di progetto, layout
delle bolle, configurazione `.env`, domande aperte con l'azienda.

## Comandi

```bash
BOLLE_EXTRACTOR=mock python -m bolle.app      # app senza rete ne' costi (rilegge gold/gold.json)
python -m bolle.app                           # app vera, http://127.0.0.1:8000
python bench/esegui.py --modello opus-5.5-api --casi reale   # banco di prova (costa: ~0,07 $/pagina con Opus)
python bench/report.py --errori               # rigenera bench/REPORT.md
```

Non ci sono test automatici (niente pytest). Per verificare la logica
deterministica si passano le pagine di `gold/gold.json` attraverso
`lavoro.costruisci_righe` / `verifica_pagina` / `excel.esporta` con uno script.

## Flusso del codice

`ingest.py` (PDF → PNG per l'operatore + JPEG per il modello) → `extract.py`
(`estrai(jpg, numero) -> PaginaEstratta`, backend `claude | openrouter | consenso | mock`)
→ `lavoro.py` (una `RigaLavoro` per taglia, controlli, avvisi) → `app.py` (FastAPI,
lettura in background) → `static/index.html` (interfaccia) → `excel.py` (fogli
`Carico` e `Tracciabilita`). Stato in SQLite (`store.py`).

## Regole di progetto da rispettare

- **Il modello legge solo lo stampato.** Le scritte a mano vanno in campi a parte
  (`annotazioni_manoscritte`, `codice_manoscritto`, `correzioni`,
  `magazzino_pagina`, `note_pagina`) e non sovrascrivono mai i campi stampati.
- **Le correzioni a mano le applica `lavoro.py`**, non il modello: quantita',
  taglie riscritte e codice a mano entrano nel carico con l'avviso
  `corretto a mano sulla bolla: ...`. Lo stampato resta in `codice_stampato`,
  `taglia_stampata`, `qta_stampata` (Tracciabilita).
- **I controlli sui totali si fanno sui valori stampati**, prima di applicare
  le correzioni (`somma(qta) == Total` di riga, `Total Pieces` di pagina).
- **Ogni dubbio diventa un avviso, mai una scelta silenziosa.** Gli avvisi sono
  stringhe; `gravita()` in `index.html` ne deduce il livello dal prefisso:
  un avviso nuovo va aggiunto anche li'.
- **Schema senza Optional**: sentinelle documentate (`""`, `0`, `-1` per "qta non
  corretta"). I campi aggiunti dopo hanno un default, cosi' il gold e le bolle
  gia' salvate restano validi.
- **Il prompt si misura, non si ritocca a occhio.** Ogni modifica a `ISTRUZIONI`
  (`bolle/extract.py`) e' una nuova versione: la precedente va salvata in
  `bench/prompt_vN.txt` e aggiunta alle scelte `--prompt` di `bench/esegui.py`.
  Versione attuale: **v4** (correzioni strutturate).
- Se cambia cio' che finisce nel carico, aggiornare anche `_firma` in
  `extract.py`: e' cio' su cui i due modelli del `consenso` devono concordare.

## Banco di prova (`bench/`)

- Casi in `bench/casi/casi.json` (37: 14 reali da `gold/gold.json`, pulite,
  sintetiche generate da `genera.py`). Le metriche (`punteggio.py`) guardano solo
  i dati del carico: codice, taglie, barrata, magazzino, correzioni.
- Non rilanciare `genera.py` per piccoli ritocchi: riscrive tutte le immagini.
  Le modifiche all'atteso si possono applicare a `casi.json` direttamente, in
  modo coerente con quello che produrrebbe `genera.py`.
- `test_data/`: ground truth dell'utente in un altro formato
  (`schema_bolla.json`, una riga per taglia, valori gia' corretti a mano), ogni
  `X.json` accanto al suo `X.pdf`. Il campo `note_estrazione` va ignorato.
  Non e' ancora collegato al banco di prova: il confronto previsto e' a livello
  di export (dopo `costruisci_righe`).

## Convenzioni

- Tutto in italiano: codice, commenti, messaggi, commit. Commenti che spiegano il
  perche', nello stile esistente; apostrofi ASCII (`e'`, `piu'`) nel codice.
- Fine riga: i sorgenti sono in CRLF in copia di lavoro (autocrlf). Gli script
  che riscrivono file devono preservare i fine riga esistenti.
- `data/` e' versionata (bolle caricate, database, export): non includerla nelle
  commit di codice se non richiesto.
- Remoto: `origin` = github.com/alessandroMacchii/progetto-bolle, branch `main`.

## Ancora aperto

- Mappa taglia → variante (`config/varianti.csv`): i codici calzatura 540, 550,
  560... sembrano mezze taglie (540=4, 550=4-, 560=5, 580=6, 620=8, 640=9) ma va
  confermato con l'azienda.
- Pagina 14 degli esempi: taglie `S/M/L` (gold) o `46/50/54` (test_data)?
  Va deciso quale colonna della Size Table leggere.
- Il prompt v4 non e' ancora stato misurato sul banco con il modello vero.
