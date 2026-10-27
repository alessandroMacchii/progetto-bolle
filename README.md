# Digitalizzazione del carico merci

Prototipo che trasforma una bolla di consegna cartacea scansionata in un file
Excel pronto per il carico massivo nel gestionale, lasciando all'operatore le
correzioni e l'assegnazione dei magazzini.

```
PDF/scansione ──► pagine normalizzate ──► estrazione ──► revisione a schermo ──► Excel
                  (rendering, rotazione)   (modello       (correzioni, MAG 1/2,   (4 colonne
                                            vision)        split, righe manuali)   + tracciabilita')
```

## Avvio rapido

```bash
pip install -r requirements.txt
cp .env.example .env          # e inserisci OPENROUTER_API_KEY (o ANTHROPIC_API_KEY)
python -m bolle.app           # poi apri http://127.0.0.1:8000
```

Per provare l'interfaccia **senza chiave e senza costi**, con i dati delle 14
pagine di esempio gia' trascritti:

```bash
BOLLE_EXTRACTOR=mock python -m bolle.app
```

## Prova online (dal PC, gratis)

Per far provare l'app all'azienda senza installare niente da loro:

```
Avvia prova online.bat        # oppure: python -m bolle.online
```

Lo script avvia l'app e apre un *quick tunnel* di Cloudflare (gratis, senza
account; `cloudflared` lo scarica da solo in `strumenti/` la prima volta). Nella
finestra stampa link, utente e password da mandare:

```
    Link:      https://<parole-a-caso>.trycloudflare.com
    Utente:    bolle
    Password:  3f1a-90bc-7e22
```

- La password viene generata al primo avvio e salvata in `.env`
  (`BOLLE_PASSWORD`): resta la stessa ai riavvii successivi.
- Il link **cambia a ogni avvio** e funziona solo finche' il PC e' acceso e la
  finestra aperta. Il PC non deve andare in sospensione.
- Il server ascolta solo su `127.0.0.1`: da fuori si entra solo dal tunnel, e
  solo con la password.
- Le bolle caricate dall'azienda restano in `data/` su questo PC.

Per l'uso vero serve un hosting: il `Dockerfile` e' pronto (dati nel volume
`/data`, `BOLLE_PASSWORD` obbligatoria, chiave API come segreto).

## Come si usa

1. Trascina la bolla (PDF multipagina o foto) nella schermata di caricamento.
2. Ogni pagina viene estratta e trasformata in **una riga per taglia**.
3. A sinistra c'e' la scansione, a destra le righe. Si correggono i campi in
   linea, si assegna il magazzino, si eliminano le righe barrate, si aggiungono
   a mano i colli arrivati senza documentazione.
4. `Esporta Excel` blocca l'export se restano righe incomplete, altrimenti
   scarica il file.

Il pallino arancione a inizio riga e' il numero di segnalazioni: passandoci
sopra si legge il motivo.

### Le azioni che contano

| Azione | A cosa serve |
|---|---|
| `MAG 1` / `MAG 2` in barra | assegna in blocco la pagina corrente (o tutte, con la spunta) |
| `Dividi` | stessa taglia su due magazzini — il caso di pagina 3 degli esempi, dove 3 pezzi vanno 2 su MAG 1 e 1 su MAG 2 |
| `Elimina` / `Ripristina` | esclude una riga senza perderla: resta nel foglio di tracciabilita' |
| `+ Riga manuale` | collo arrivato senza documentazione |
| `Ruota` | raddrizza una scansione coricata |

## Scelte di progetto

**Il modello legge solo lo stampato.** Le scritte a penna vengono trascritte in
un campo a parte e non sovrascrivono mai un dato stampato. Un `MAG 2` letto male
da una calligrafia e' un errore che finisce dritto in magazzino; un `MAG 2`
sbagliato in interfaccia lo vede l'operatore. Quando l'annotazione nomina un
solo magazzino il campo viene comunque **precompilato**, con una segnalazione da
confermare; quando ne nomina piu' di uno (pagina 3) non si indovina: si segnala.

**Due checksum gratuiti.** Ogni riga stampa il proprio totale e ogni pagina il
`Total Pieces`. `somma(quantita') == Total` e' una verifica che non costa nulla
e intercetta gli errori di lettura da sola: le righe che non quadrano vengono
evidenziate. Sulle 14 pagine di esempio tutte le 33 righe quadrano.

**Estrazione a backend intercambiabile.** Il resto dell'applicazione conosce
solo `estrai(jpg, numero) -> PaginaEstratta`. Vedi "Portare tutto in casa".

**Doppio foglio nell'export.** Il foglio `Carico` ha esattamente le quattro
colonne richieste, niente altro: e' il file da dare all'import. Il foglio
`Tracciabilita` conserva pagina, seq, descrizione, colore, origine e note, per
capire a mesi di distanza da dove viene un carico.

## Formati riconosciuti

Tutte le bolle vengono dallo stesso fornitore, ma nelle 14 pagine di esempio
convivono sei impaginazioni:

| Layout | Pagine di esempio | Caratteristica |
|---|---|---|
| `DELIVERY NOTE` standard | 1, 4, 9, 13 | tabella Seq-no / Article / Name / Total / Size-Qty + box SUMMARY |
| `DELIVERY NOTE` compatto | 8, 10, 12 | piu' articoli sotto un solo blocco "Order From", totali in coda |
| `DELIVERY NOTE` ad aghi | 2, 6 | font monospace, colonne allineate diversamente |
| `CONSOLIDATED ORDER NUMBER` | 3 | intestazione diversa, DN Number dentro la cella |
| `Value Added Service` | 5 | colonne del tutto diverse, pagina coricata |
| `mi adidas Product Specification` | 11, 14 | niente tabella righe: Size Table verticale |

### La colonna Size/Qty

Sequenza di token `TAGLIA/QUANTITA`. Il parser (`bolle/sizes.py`) e' verificato
su tutte le stringhe reali degli esempi:

```
8-/2                  mezza taglia calzatura
9-/3 11-/1            piu' taglie sulla stessa riga
XS/2 S/7 M/10 L/8     abbigliamento
XS/183 XL/50          quantita' a tre cifre
NS/5                  taglia unica
7-8A/6 910A/5 1112/5  taglie bambino in anni
540/3 560/6           codici numerici calzatura
```

## Domande ancora aperte con l'azienda

Sono i punti che il codice non puo' decidere da solo. I primi due vanno chiusi
prima di usare il prototipo sul serio.

1. **Come si chiama la "Variante" nel gestionale?** E' la taglia? Taglia e
   colore? Serve la corrispondenza `taglia bolla -> codice variante`. Finche'
   non arriva, la mappa vive in `config/varianti.csv` (modificabile senza
   toccare il codice) e tutto cio' che non e' mappato passa invariato **con una
   segnalazione in interfaccia**. Le regole provvisorie attive:
   - `8-` -> `8.5` (mezza taglia) — **da confermare**
   - `910A` -> `9-10A`, `1112` -> `11-12A` (taglie in anni) — **da confermare**
   - `540`, `560`, `620` — passano invariate, non sappiamo cosa significhino
2. **Formato esatto del file di import**: nomi colonna, ordine, header si'/no.
   Configurabile con `BOLLE_EXCEL_HEADERS`. Serve un file di esempio funzionante.
3. **Esiste un export dell'anagrafica articoli dal gestionale?** Sarebbe la
   differenza piu' grande: validerebbe i codici letti e risolverebbe le varianti.
4. **La regola di assegnazione magazzino e' arbitraria o segue una logica?**
   (per categoria, per ordine, per cliente finale)
5. Come arrivano le bolle: scanner multifunzione o foto da telefono?

## Misurare l'accuratezza

`gold/gold.json` e' la trascrizione manuale delle 14 pagine di esempio. Serve a
sapere se il prototipo funziona e a non peggiorarlo la prossima volta che si
tocca il prompt.

```bash
python scripts/eval_extraction.py "Esempio bolle.pdf" --solo-coerenza   # verifica il gold set
python scripts/eval_extraction.py "Esempio bolle.pdf"                   # misura l'estrazione
python scripts/eval_extraction.py "Esempio bolle.pdf" --pagine 3,5,14   # solo i casi difficili
```

Confronta 164 controlli: numero documento, Total Pieces, rotazione, numero di
righe, e per ogni riga codice articolo, taglie, totale e barratura.

> Il gold set e' una trascrizione umana e puo' contenere errori. A suo favore:
> tutte le 33 righe superano il controllo `somma(qta) == Total`, che e' una
> verifica indipendente da chi ha trascritto.

## Portare tutto in casa

Oggi l'estrazione usa Opus 5.5 via API. Costi misurati sul banco di prova
(`bench/REPORT.md`): ~0,07 $ a pagina con Opus 5.5, ~0,037 $ con Sonnet 5.5, che
pero' sbaglia di piu' sulla calligrafia vera (10/14 pagine perfette contro
13/14). Le alternative offline, valutate:

| Strada | Requisiti | Stato |
|---|---|---|
| Modello addestrato su misura (Donut, LayoutLM) | migliaia di bolle etichettate | non ora: ne abbiamo 14. Diventa possibile con lo storico che il prototipo stesso accumula |
| VLM locale (Qwen2.5-VL, InternVL) | GPU da 8-16 GB | fattibile su una macchina con GPU |
| OCR classico (Tesseract/PaddleOCR) + regole | nessuno | fattibile, ma sei template da mantenere, fragile sul settimo layout e sulle pagine coperte dalle penne |

Per innestarne uno basta implementare `EstrattoreLocale.estrai()` in
`bolle/extract.py` e mettere `BOLLE_EXTRACTOR=local`: interfaccia, validazioni
ed export non cambiano.

## Struttura

```
bolle/
  config.py    percorsi, magazzini, colonne export (tutto da .env)
  ingest.py    PDF/immagine -> PNG per l'operatore + JPEG per il modello, rotazione
  schema.py    struttura dei dati estratti e delle righe di lavoro
  extract.py   estrattori intercambiabili: claude | mock | local
  sizes.py     parsing Size/Qty, checksum, mappa taglia -> variante
  lavoro.py    da pagina estratta a righe editabili, con le segnalazioni
  store.py     persistenza SQLite (stato completo, ri-esportabile)
  excel.py     generazione del file di import + tracciabilita'
  app.py       server FastAPI (lettura delle pagine in background e in parallelo)
  online.py    prova online: app + tunnel Cloudflare + password
  static/      interfaccia operatore
gold/          trascrizione di riferimento delle 14 pagine
scripts/       misura dell'accuratezza
config/        varianti.csv, la mappa taglia -> variante da compilare
data/          runtime: upload, pagine renderizzate, database, export
```

## Configurazione

Tutto da `.env`:

| Variabile | Default | Note |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | necessaria con `BOLLE_EXTRACTOR=claude` |
| `BOLLE_EXTRACTOR` | `claude` | `claude` \| `openrouter` \| `mock` \| `local` |
| `OPENROUTER_API_KEY` | — | necessaria con `BOLLE_EXTRACTOR=openrouter` e per i modelli OpenRouter del banco di prova |
| `BOLLE_OPENROUTER_MODEL` | `anthropic/claude-opus-5.5` | id del modello su openrouter.ai/models |
| `BOLLE_MODEL` | `claude-opus-5-5` | con `BOLLE_EXTRACTOR=claude`; `claude-sonnet-5-5` costa circa la meta' |
| `BOLLE_PARALLELO` | `4` | pagine lette in contemporanea |
| `BOLLE_PASSWORD` | — | se impostata, il browser chiede utente e password. Online e' obbligatoria |
| `BOLLE_UTENTE` | `bolle` | nome utente del login |
| `BOLLE_HOST` / `PORT` | `127.0.0.1` / `8000` | nel container `0.0.0.0` |
| `BOLLE_DATA_DIR` | `data/` | database, scansioni, export |
| `BOLLE_MAGAZZINI` | `MAG 1,MAG 2` | i magazzini selezionabili |
| `BOLLE_EXCEL_HEADERS` | `Magazzino,Codice Articolo,Variante,Quantita` | intestazioni del foglio di import |
| `BOLLE_RENDER_DPI` | `200` | risoluzione della scansione a schermo |
| `BOLLE_API_MAX_EDGE` | `1600` | lato lungo dell'immagine inviata al modello |

## Limiti noti

- L'euristica di rotazione indovina 12 pagine su 14 e non sa dire il verso; il
  valore buono e' quello che riporta il modello, e resta il pulsante `Ruota`.
- Una bolla su piu' pagine viene trattata come pagine indipendenti: il totale di
  pagina 7 degli esempi non quadra perche' il seguito non c'e' nella scansione.
  L'interfaccia lo segnala; l'operatore lo capisce.
- Un solo utente e password condivisi (`BOLLE_PASSWORD`), nessun ruolo. In
  locale, senza password, nessuna autenticazione.
- Le righe senza un magazzino scritto a mano vanno su `MAG 1` per default:
  da confermare con l'azienda (domanda 4).
- Se il server si riavvia mentre legge una bolla, quella bolla risulta
  interrotta e va ricaricata.
- Le immagini escono verso l'API del modello. Da verificare se e' accettabile
  (vedi "Portare tutto in casa").
