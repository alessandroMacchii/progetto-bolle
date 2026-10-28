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

1. Alla prima apertura l'app chiede "Chi sta lavorando?" (con i nomi gia'
   usati da scegliere con un clic; il browser lo ricorda, si cambia dal
   pulsante con le iniziali in alto). Poi trascina la bolla (PDF multipagina o foto)
   nella schermata di caricamento, oppure fotografala con `Scansiona con la
   fotocamera` (vedi sotto).
2. Ogni pagina viene estratta e trasformata in **una riga per taglia**.
3. A sinistra c'e' la scansione, a destra le righe. Si correggono i campi in
   linea (codice, descrizione, taglia, variante, quantita'), si assegna il
   magazzino, si eliminano le righe barrate, si aggiungono a mano i colli
   arrivati senza documentazione.
4. `Esporta Excel` blocca l'export se restano righe incomplete, altrimenti
   scarica il file. Bloccano ogni riga attiva senza codice, senza magazzino (o
   con un magazzino che non e' fra quelli configurati) e con la taglia da
   validare: una taglia fuori da `config/varianti.csv` va confermata o
   corretta prima dell'export. Cambiando a mano la taglia, la variante si
   ricalcola dal CSV.

Il pallino arancione a inizio riga e' il numero di segnalazioni: passandoci
sopra si legge il motivo.

**Bolle caricate due volte.** Un file identico a uno gia' caricato si ferma
prima della lettura (che costa): si sceglie se aprire quello esistente o
rileggerlo. Se invece il file e' diverso ma il numero di documento e' gia' in
un'altra bolla (una foto e un PDF della stessa), la revisione lo segnala con
data, operatore ed eventuale export dell'altra: esportarle entrambe conterebbe
la merce due volte. Nella tendina ogni bolla mostra numero di documento, data
di caricamento, operatore e data dell'export.

### Le azioni che contano

| Azione | A cosa serve |
|---|---|
| `MAG 1` / `MAG 2` in barra | assegna in blocco la pagina corrente (o tutte, con la spunta) |
| `Dividi` | stessa taglia su due magazzini — il caso di pagina 3 degli esempi, dove 3 pezzi vanno 2 su MAG 1 e 1 su MAG 2 |
| `Verificata` (spunta) | ho controllato la scansione e gli avvisi della riga tornano: la riga esce dalle "Da controllare", gli avvisi restano nella tracciabilita'. Non sblocca i dati mancanti (codice, magazzino, taglia da validare) |
| `Elimina` / `Ripristina` | esclude una riga senza perderla: resta nel foglio di tracciabilita' |
| `+ Riga manuale` | collo arrivato senza documentazione |
| `Ruota` | raddrizza una scansione coricata |

### Scansionare dalla fotocamera

Dal telefono o dal tablet, senza scanner:

1. **Scatto.** La fotocamera si apre nella pagina; quando il contorno arancione
   aggancia il foglio e resta fermo per circa un secondo, scatta da sola (lo
   scatto automatico si spegne dalla pillola). `Dalle foto` prende foto gia'
   fatte, anche piu' di una alla volta.
2. **Ritaglio.** I quattro angoli trovati si correggono trascinando le
   maniglie; mentre si trascina, una lente ingrandisce il punto sotto il dito.
   Da tastiera: Tab sulla maniglia e frecce (Maiuscolo per passi lunghi).
3. **Pagina pronta.** `Migliorata` (predefinita) toglie ombre e dominante
   gialla e alza il contrasto restando **a colori**: niente bianco e nero da
   scanner, che cancellerebbe evidenziatore, matita e penna rossa. `Originale`
   tiene la foto solo raddrizzata.
4. `Altra pagina` per le bolle di piu' fogli, poi `Leggi la bolla`: da li' e'
   come aver caricato un PDF.

Bordi, raddrizzamento e miglioramento sono visione artificiale classica
(OpenCV, `bolle/scan.py`), senza modelli: pochi millisecondi per il
rilevamento, una frazione di secondo per pagina per il resto. In `data/uploads`
restano le foto originali (`<id>_foto_pNN.jpg`, per rifare il ritaglio) e il
PDF delle pagine elaborate.

La fotocamera nella pagina richiede HTTPS o `localhost`: va col tunnel della
prova online e sul PC, non con `http://192.168.x.x`. Dove non e' disponibile,
la schermata offre `Scatta una foto`, che sul telefono apre la fotocamera di
sistema.

## Scelte di progetto

**Il modello legge lo stampato, il programma applica le correzioni a mano.**
Il modello non sovrascrive mai un dato stampato: le scritte a penna le restituisce
a parte (`annotazioni_manoscritte`, `codice_manoscritto` e, in forma strutturata,
`correzioni`). Poi `lavoro.py` le applica **da solo** e lascia un segnale su ogni
modifica:
- quantita' corrette (pagina 8: XS 6 -> 5), taglie riscritte a mano sopra quelle
  stampate (pagina 2: 550 -> 4-) e codici scritti a mano entrano nel carico al
  posto dello stampato, con la segnalazione `corretto a mano sulla bolla: ...`
  da confermare. Lo stampato resta visibile in interfaccia e nel foglio
  `Tracciabilita`;
- una correzione che non trova la sua taglia stampata non viene applicata ma
  segnalata;
- se la cifra scritta a mano e' ambigua il modello non la riporta fra le
  correzioni: la spiega in `incertezze` e decide l'operatore.

I magazzini seguono la stessa logica. Quando l'annotazione nomina un solo
magazzino il campo viene **precompilato**, con una segnalazione da confermare;
quando ne nomina piu' di uno (pagina 3) non si indovina: si segnala.
Se la scritta e' riferita a singole taglie, o divide i pezzi di una stessa
taglia fra piu' magazzini, il modello la riporta in `magazzini_per_taglia`
(taglia stampata, magazzino, pezzi) e `lavoro.py` divide la taglia in piu'
righe, una per magazzino. Se i pezzi non tornano con la quantita' della taglia
la riga resta intera e senza magazzino; i pezzi senza sigla restano senza
magazzino. In entrambi i casi decide l'operatore.

**Due checksum gratuiti.** Ogni riga stampa il proprio totale e ogni pagina il
`Total Pieces`. `somma(quantita') == Total` e' una verifica che non costa nulla
e intercetta gli errori di lettura da sola: le righe che non quadrano vengono
evidenziate. Sulle 14 pagine di esempio tutte le 33 righe quadrano.

**Due modelli economici, uno forte quando non concordano** (`BOLLE_EXTRACTOR=consenso`).
Gemini 3.8 Flash e Haiku 5.5 leggono ogni pagina in parallelo; se concordano su
codici, taglie, barrate e magazzini si tiene la lettura, altrimenti la pagina
passa a Opus 5.5. Due modelli diversi raramente sbagliano allo stesso modo, quindi
il disaccordo intercetta anche gli errori che il modello non sa di fare. Sul banco
di prova, prompt v3: 36/37 pagine perfette e 14/14 sulla calligrafia vera (Opus da
solo 35/37), 0 errori non segnalati, 0,033 $/pagina invece di 0,070. Col prompt v2,
dal vivo sulle 14 pagine reali, meta' delle pagine erano passate a Opus: li' il
costo sale verso 0,05 $/pagina.

**Il prompt si misura, non si ritocca a occhio.** v1 -> v2 -> v3 -> v4 passano tutti
dal banco di prova (`bench/`); i precedenti restano in `bench/prompt_v1.txt`,
`bench/prompt_v2.txt` e `bench/prompt_v3.txt`. Il v4 aggiunge le `correzioni`
strutturate (colonna "correzioni a mano" del report). Il v3 aveva aggiunto: barrata anche con una sola X sul Seq-no,
MAG non barrato su una riga barrata alla riga attiva vicina, MAG sopra le taglie
alla riga di quelle taglie, niente segnalazioni su quantita' gia' confermate dal
Total o su campi fuori dal carico.
Ogni pagina registra chi l'ha letta (campo `motore`), per misurarlo nella prova.

**Estrazione a backend intercambiabile.** Il resto dell'applicazione conosce
solo `estrai(jpg, numero) -> PaginaEstratta`. Vedi "Portare tutto in casa".

**Tre fogli nell'export.** Il foglio `Carico` ha esattamente le quattro
colonne richieste, niente altro: e' il file da dare all'import. Il foglio
`Tracciabilita` conserva pagina, seq, descrizione, colore, origine e note, per
capire a mesi di distanza da dove viene un carico, con chi ha caricato la bolla
e chi ha modificato ogni riga. Il foglio `Modifiche` e' il registro completo:
quando, chi, cosa (caricamento, correzioni campo per campo con il valore prima
e dopo, divisioni, varianti confermate, export).

**L'operatore non e' un login.** L'accesso resta uno per tutti; il nome
scelto in "Chi sta lavorando?" viaggia con ogni richiesta (header `X-Operatore`) e il
server rifiuta caricamenti, modifiche ed export senza. Serve alla
tracciabilita', non alla sicurezza: chiunque abbia l'accesso puo' scrivere
qualunque nome.

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
   segnalazione in interfaccia**. Il codice fa solo due uniformazioni, senza
   avvisi: il maiuscolo e le taglie in anni nella forma `5-6A` (`910A` ->
   `9-10A`, `1112` -> `11-12A`), cosi' nel CSV basta una voce per taglia. Mezze
   taglie (`8-`) e codici calzatura (`540`, `560`, `620`) passano invariati
   finche' non compaiono nel CSV. L'operatore puo'
   confermarli o correggerli dall'interfaccia: la coppia taglia -> variante
   viene aggiunta al CSV e applicata a tutte le righe del documento con la
   stessa taglia.
2. **Formato esatto del file di import**: nomi colonna, ordine, header si'/no.
   Configurabile con `BOLLE_EXCEL_HEADERS`. Serve un file di esempio funzionante.
3. **Esiste un export dell'anagrafica articoli dal gestionale?** Sarebbe la
   differenza piu' grande: validerebbe i codici letti e risolverebbe le varianti.
4. **La regola di assegnazione magazzino e' arbitraria o segue una logica?**
   (per categoria, per ordine, per cliente finale)
5. Come arrivano le bolle: scanner multifunzione o foto da telefono?

## Misurare l'accuratezza

Il banco di prova in `bench/` misura ogni modello e ogni versione del prompt su
37 casi (le 14 pagine reali di `gold/gold.json` piu' pagine sintetiche e nuove
bolle). Serve a non peggiorare l'estrazione la prossima volta che si tocca il
prompt.

```bash
python bench/esegui.py --modello opus-5.5-api            # esegue un modello
python bench/esegui.py --modello gemini-3.8-flash --casi reale   # solo una famiglia
python bench/report.py --errori                          # rigenera bench/REPORT.md
```

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

Per innestarne uno basta una classe con il metodo `estrai(jpg, numero)` in
`bolle/extract.py`, registrata in `crea_estrattore`: interfaccia, validazioni
ed export non cambiano.

## Struttura

```
bolle/
  config.py    percorsi, magazzini, colonne export (tutto da .env)
  ingest.py    PDF/immagine -> PNG per l'operatore + JPEG per il modello, rotazione
  scan.py      foto da fotocamera -> bordi del foglio, raddrizzamento, pulizia
  schema.py    struttura dei dati estratti e delle righe di lavoro
  extract.py   estrattori intercambiabili: claude | openrouter | consenso | mock
  sizes.py     parsing Size/Qty, checksum, mappa taglia -> variante
  lavoro.py    da pagina estratta a righe editabili, con le segnalazioni
  store.py     persistenza SQLite (stato completo, ri-esportabile)
  excel.py     generazione del file di import + tracciabilita'
  app.py       server FastAPI (lettura delle pagine in background e in parallelo)
  online.py    prova online: app + tunnel Cloudflare + password
  static/      interfaccia operatore
gold/          trascrizione di riferimento delle 14 pagine
bench/         banco di prova: casi, prompt precedenti, risultati, report
config/        varianti.csv, la mappa taglia -> variante da compilare
data/          runtime: upload, pagine renderizzate, database, export
```

## Configurazione

Tutto da `.env`:

| Variabile | Default | Note |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | necessaria con `BOLLE_EXTRACTOR=claude` |
| `BOLLE_EXTRACTOR` | `claude` | `claude` \| `openrouter` \| `consenso` \| `mock` |
| `BOLLE_CONSENSO_MODELLI` | `google/gemini-3.8-flash,anthropic/claude-haiku-5.5` | i due lettori economici del consenso |
| `BOLLE_CONSENSO_ARBITRO` | `anthropic/claude-opus-5.5` | chi legge quando i due non concordano |
| `OPENROUTER_API_KEY` | — | necessaria con `BOLLE_EXTRACTOR=openrouter` e per i modelli OpenRouter del banco di prova |
| `BOLLE_OPENROUTER_MODEL` | `anthropic/claude-opus-5.5` | id del modello su openrouter.ai/models |
| `BOLLE_MODEL` | `claude-opus-5-5` | con `BOLLE_EXTRACTOR=claude`; `claude-sonnet-5-5` costa circa la meta' |
| `BOLLE_PARALLELO` | `4` | pagine lette in contemporanea |
| `BOLLE_PASSWORD` | — | se impostata, il browser chiede utente e password. Online e' obbligatoria |
| `BOLLE_UTENTE` | `bolle` | nome utente del login |
| `BOLLE_IP_HEADER` | — | header con l'IP vero dietro un proxy fidato (`cf-connecting-ip` col tunnel, lo imposta `bolle.online`). Serve al blocco dopo 10 password sbagliate |
| `BOLLE_MAX_MB` / `BOLLE_MAX_PAGINE` | `40` / `60` | tetti sull'upload |
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
- Le righe senza un magazzino scritto a mano restano senza magazzino: l'export
  si blocca finche' l'operatore non lo assegna (anche in massa, per pagina o
  documento). Da confermare con l'azienda (domanda 4).
- Se il server si riavvia mentre legge una bolla, quella bolla risulta
  interrotta e va ricaricata.
- Le immagini escono verso l'API del modello. Da verificare se e' accettabile
  (vedi "Portare tutto in casa").
