# Confronto modelli sul banco di prova

20 casi: 330 taglie di carico. Generato da `python bench/report.py`.

## Complessivo

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | correzioni a mano | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| consenso | 15/20 | 95% | 99% | 98% | 25/38 | 0/0 | 0/0 | 4 | 0 | 8 (6 a vuoto) | $0.0380 | 25 |
| opus-5.5-api | 15/20 | 95% | 99% | 98% | 25/38 | 0/0 | 0/0 | 4 | 0 | 10 (8 a vuoto) | $0.0648 | 18 |

## Caso per caso (righe perfette / righe)

| caso | cosa prova | consenso | opus-5.5-api |
|---|---|---|---|
| td-adidas_nuova | ground truth di test_data (Adidas_nuova) | 69/71 ⚠ | 69/71 ⚠ |
| td-esempio-bolle-1 | ground truth di test_data (Esempio bolle-1) | 1/1 | 1/1 |
| td-esempio-bolle-10 | ground truth di test_data (Esempio bolle-10) | 1/1 | 1/1 |
| td-esempio-bolle-11 | ground truth di test_data (Esempio bolle-11) | 3/3 | 3/3 |
| td-esempio-bolle-12 | ground truth di test_data (Esempio bolle-12) | 5/8 | 5/8 |
| td-esempio-bolle-13 | ground truth di test_data (Esempio bolle-13) | 1/1 | 1/1 |
| td-esempio-bolle-14 | ground truth di test_data (Esempio bolle-14) | 0/3 | 0/3 |
| td-esempio-bolle-2 | ground truth di test_data (Esempio bolle-2) | 2/5 | 2/5 |
| td-esempio-bolle-3 | ground truth di test_data (Esempio bolle-3) | 0/4 | 0/4 |
| td-esempio-bolle-4 | ground truth di test_data (Esempio bolle-4) | 4/4 | 4/4 |
| td-esempio-bolle-5 | ground truth di test_data (Esempio bolle-5) | 3/3 | 3/3 |
| td-esempio-bolle-6 | ground truth di test_data (Esempio bolle-6) | 2/2 | 2/2 |
| td-esempio-bolle-7 | ground truth di test_data (Esempio bolle-7) | 2/2 | 2/2 |
| td-esempio-bolle-8 | ground truth di test_data (Esempio bolle-8) | 1/1 | 1/1 |
| td-esempio-bolle-9 | ground truth di test_data (Esempio bolle-9) | 2/2 | 2/2 |
| td-pulita1 | ground truth di test_data (pulita1) | 21/21 | 21/21 |
| td-pulita2_1 | ground truth di test_data (pulita2_1) | 47/47 | 47/47 |
| td-pulita2_2 | ground truth di test_data (pulita2_2) | 55/55 | 55/55 |
| td-pulita2_3 | ground truth di test_data (pulita2_3) | 39/39 | 39/39 |
| td-pulita2_4 | ground truth di test_data (pulita2_4) | 34/34 | 34/34 |

⚠ = almeno un errore silenzioso (non intercettato dal checksum).

- **consenso**: Modalita' consenso dell'app (Gemini 3.8 Flash + Haiku 5.5, arbitro Opus 5.5), prompt v4, via OpenRouter.
  Pagine passate all'arbitro: 6 su 20.

- **opus-5.5-api**: Prompt v4 sul ground truth di test_data, via OpenRouter.

## Errori

### consenso

- `td-adidas_nuova`: KH5610 taglia 6 qta: attesa 2, letta 1
- `td-adidas_nuova`: KH5610 taglia 7- qta: attesa 2, letta 1
- `td-adidas_nuova`: in piu' nel carico: KH5610 taglia 6- qta 1
- `td-adidas_nuova`: in piu' nel carico: KH5610 taglia 7 qta 1
- `td-esempio-bolle-12`: JN5469 taglia M MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-12`: JN5469 taglia L MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-12`: JN5469 taglia 3XL MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-14`: JM9191 taglia 46 MAG 1 (qta 2) mancante nel carico
- `td-esempio-bolle-14`: JM9191 taglia 50 MAG 1 (qta 2) mancante nel carico
- `td-esempio-bolle-14`: JM9191 taglia 54 MAG 1 (qta 1) mancante nel carico
- `td-esempio-bolle-14`: in piu' nel carico: JN9131 taglia S qta 2 MAG 1
- `td-esempio-bolle-14`: in piu' nel carico: JN9131 taglia M qta 2 MAG 1
- `td-esempio-bolle-14`: in piu' nel carico: JN9131 taglia L qta 1 MAG 1
- `td-esempio-bolle-2`: IF4076 taglia 6 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-2`: IF4076 taglia 8 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-2`: IF4076 taglia 9 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 8 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 11- MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 9- MAG 1 qta: attesa 2, letta 3
- `td-esempio-bolle-3`: IH4278 taglia 9- MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 9- MAG 2 (qta 1) mancante nel carico

### opus-5.5-api

- `td-adidas_nuova`: KH5610 taglia 6 qta: attesa 2, letta 1
- `td-adidas_nuova`: KH5610 taglia 7- qta: attesa 2, letta 1
- `td-adidas_nuova`: in piu' nel carico: KH5610 taglia 6- qta 1
- `td-adidas_nuova`: in piu' nel carico: KH5610 taglia 7 qta 1
- `td-esempio-bolle-12`: JN5469 taglia M MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-12`: JN5469 taglia L MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-12`: JN5469 taglia 3XL MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-14`: JM9191 taglia 46 MAG 1 (qta 2) mancante nel carico
- `td-esempio-bolle-14`: JM9191 taglia 50 MAG 1 (qta 2) mancante nel carico
- `td-esempio-bolle-14`: JM9191 taglia 54 MAG 1 (qta 1) mancante nel carico
- `td-esempio-bolle-14`: in piu' nel carico: JN9131 taglia S qta 2 MAG 1
- `td-esempio-bolle-14`: in piu' nel carico: JN9131 taglia M qta 2 MAG 1
- `td-esempio-bolle-14`: in piu' nel carico: JN9131 taglia L qta 1 MAG 1
- `td-esempio-bolle-2`: IF4076 taglia 6 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-2`: IF4076 taglia 8 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-2`: IF4076 taglia 9 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 8 MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 11- MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 9- MAG 1 qta: attesa 2, letta 3
- `td-esempio-bolle-3`: IH4278 taglia 9- MAG 1 magazzino: atteso MAG 1, letto -
- `td-esempio-bolle-3`: IH4278 taglia 9- MAG 2 (qta 1) mancante nel carico
