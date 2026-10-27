# Confronto modelli sul banco di prova

37 casi, 268 righe di bolla. Generato da `python bench/report.py`.

## Complessivo

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 26/37 | 85% | 100% | 97% | 127/155 (+1 inventati) | 12/15 | 8 | 8 | 0 (0 a vuoto) | $0.0167 | 32 |
| gemini-3.8-flash prompt v2 | 31/37 | 97% | 100% | 100% | 150/155 (+2 inventati) | 15/15 | 2 | 1 | 2 (1 a vuoto) | $0.0159 | 27 |
| gemini-3.8-flash prompt v3 | 32/37 | 96% | 99% | 100% | 150/155 (+2 inventati) | 15/15 | 4 | 4 | 5 (5 a vuoto) | $0.0148 | 20 |
| gemini-pro prompt v1 | 26/37 | 88% | 100% | 96% | 140/155 (+1 inventati) | 9/15 | 10 | 10 | 0 (0 a vuoto) | $0.0589 | 38 |
| gemini-pro prompt v2 | 32/37 | 97% | 100% | 99% | 152/155 (+1 inventati) | 15/15 | 3 | 0 | 11 (8 a vuoto) | $0.0691 | 41 |
| haiku-4.5 prompt v1 | 8/37 | 38% | 89% | 79% | 29/155 (+1 inventati) | 1/15 | 14 | 14 | 0 (0 a vuoto) | $0.0082 | n.d. |
| haiku-5.5 prompt v2 | 24/37 | 90% | 99% | 99% | 141/155 (+2 inventati) | 10/15 | 5 | 1 | 49 (45 a vuoto) | $0.0025 | 15 |
| haiku-5.5 prompt v3 | 28/37 | 93% | 99% | 99% | 142/155 | 14/15 | 6 | 2 | 27 (23 a vuoto) | $0.0026 | 15 |
| locale-qwen3.5-0.8b (4 casi su 37) | 0/4 | 32% | 36% | 32% | 0/0 | 0/0 | 19 | 19 | 0 (0 a vuoto) | $0.0000 | 210 |
| opus-5.5 prompt v1 | 34/37 | 99% | 100% | 100% | 153/155 (+1 inventati) | 15/15 | 1 | 1 | 0 (0 a vuoto) | $0.0355 | n.d. |
| opus-5.5 prompt v2 | 35/37 | 99% | 100% | 100% | 153/155 (+1 inventati) | 15/15 | 0 | 0 | 41 (41 a vuoto) | $0.0386 | n.d. |
| opus-5.5-api prompt v2 | 34/37 | 99% | 100% | 100% | 153/155 (+2 inventati) | 15/15 | 0 | 0 | 21 (21 a vuoto) | $0.0699 | 24 |
| opus-5.5-api prompt v3 | 35/37 | 99% | 100% | 100% | 153/155 | 15/15 | 0 | 0 | 14 (14 a vuoto) | $0.0700 | 23 |
| sonnet-5.5 prompt v1 | 31/37 | 97% | 99% | 99% | 154/155 (+2 inventati) | 15/15 | 5 | 5 | 0 (0 a vuoto) | $0.0176 | n.d. |
| sonnet-5.5 prompt v2 | 32/37 | 98% | 99% | 100% | 153/155 | 15/15 | 3 | 0 | 24 (21 a vuoto) | $0.0188 | n.d. |
| sonnet-5.5-api prompt v2 | 32/37 | 98% | 100% | 100% | 152/155 (+1 inventati) | 15/15 | 2 | 0 | 21 (19 a vuoto) | $0.0370 | 14 |

## Calligrafia vera (14 pagine di esempio)

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 10/14 | 74% | 96% | 96% | 16/17 (+1 inventati) | 5/8 | 2 | 2 | 0 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v2 | 11/14 | 85% | 96% | 96% | 16/17 (+1 inventati) | 8/8 | 2 | 1 | 1 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v3 | 12/14 | 89% | 100% | 96% | 16/17 (+1 inventati) | 8/8 | 1 | 1 | 1 (1 a vuoto) |  |  |
| gemini-pro prompt v1 | 10/14 | 63% | 100% | 93% | 16/17 (+1 inventati) | 2/8 | 2 | 2 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v2 | 12/14 | 93% | 96% | 96% | 17/17 | 8/8 | 2 | 0 | 3 (1 a vuoto) |  |  |
| haiku-4.5 prompt v1 | 4/14 | 37% | 81% | 59% | 13/17 (+1 inventati) | 0/8 | 8 | 8 | 0 (0 a vuoto) |  |  |
| haiku-5.5 prompt v2 | 8/14 | 59% | 96% | 89% | 16/17 (+1 inventati) | 3/8 | 4 | 0 | 16 (12 a vuoto) |  |  |
| haiku-5.5 prompt v3 | 9/14 | 78% | 96% | 89% | 16/17 | 7/8 | 4 | 1 | 13 (10 a vuoto) |  |  |
| opus-5.5 prompt v1 | 12/14 | 89% | 96% | 100% | 16/17 (+1 inventati) | 8/8 | 1 | 1 | 0 (0 a vuoto) |  |  |
| opus-5.5 prompt v2 | 13/14 | 93% | 100% | 100% | 16/17 (+1 inventati) | 8/8 | 0 | 0 | 15 (15 a vuoto) |  |  |
| opus-5.5-api prompt v2 | 13/14 | 93% | 100% | 100% | 16/17 (+1 inventati) | 8/8 | 0 | 0 | 9 (9 a vuoto) |  |  |
| opus-5.5-api prompt v3 | 14/14 | 100% | 100% | 100% | 17/17 | 8/8 | 0 | 0 | 8 (8 a vuoto) |  |  |
| sonnet-5.5 prompt v1 | 10/14 | 81% | 93% | 96% | 16/17 (+1 inventati) | 8/8 | 3 | 3 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v2 | 11/14 | 89% | 93% | 96% | 17/17 | 8/8 | 3 | 0 | 13 (10 a vuoto) |  |  |
| sonnet-5.5-api prompt v2 | 10/14 | 81% | 96% | 96% | 15/17 (+1 inventati) | 8/8 | 2 | 0 | 12 (10 a vuoto) |  |  |

## Bolle bianche (altrebolle/)

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v3 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| haiku-4.5 prompt v1 | 3/4 | 96% | 100% | 96% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| haiku-5.5 prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 5 (5 a vuoto) |  |  |
| haiku-5.5 prompt v3 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 1 (1 a vuoto) |  |  |
| locale-qwen3.5-0.8b | 0/4 | 32% | 36% | 32% | 0/0 | 0/0 | 19 | 19 | 0 (0 a vuoto) |  |  |
| opus-5.5 prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| opus-5.5 prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| opus-5.5-api prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| opus-5.5-api prompt v3 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| sonnet-5.5-api prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |

## Varianti con annotazioni disegnate

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 12/19 | 83% | 100% | 97% | 111/138 | 7/7 | 6 | 6 | 0 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v2 | 16/19 | 97% | 100% | 100% | 134/138 (+1 inventati) | 7/7 | 0 | 0 | 1 (1 a vuoto) |  |  |
| gemini-3.8-flash prompt v3 | 16/19 | 96% | 98% | 100% | 134/138 (+1 inventati) | 7/7 | 3 | 3 | 4 (4 a vuoto) |  |  |
| gemini-pro prompt v1 | 12/19 | 89% | 100% | 96% | 124/138 | 7/7 | 8 | 8 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v2 | 16/19 | 97% | 100% | 99% | 135/138 (+1 inventati) | 7/7 | 1 | 0 | 8 (7 a vuoto) |  |  |
| haiku-4.5 prompt v1 | 1/19 | 24% | 88% | 77% | 16/138 | 1/7 | 6 | 6 | 0 (0 a vuoto) |  |  |
| haiku-5.5 prompt v2 | 12/19 | 92% | 99% | 99% | 125/138 (+1 inventati) | 7/7 | 1 | 1 | 28 (28 a vuoto) |  |  |
| haiku-5.5 prompt v3 | 15/19 | 93% | 99% | 99% | 126/138 | 7/7 | 2 | 1 | 13 (12 a vuoto) |  |  |
| opus-5.5 prompt v1 | 18/19 | 99% | 100% | 100% | 137/138 | 7/7 | 0 | 0 | 0 (0 a vuoto) |  |  |
| opus-5.5 prompt v2 | 18/19 | 99% | 100% | 100% | 137/138 | 7/7 | 0 | 0 | 26 (26 a vuoto) |  |  |
| opus-5.5-api prompt v2 | 17/19 | 99% | 100% | 100% | 137/138 (+1 inventati) | 7/7 | 0 | 0 | 12 (12 a vuoto) |  |  |
| opus-5.5-api prompt v3 | 17/19 | 99% | 100% | 100% | 136/138 | 7/7 | 0 | 0 | 6 (6 a vuoto) |  |  |
| sonnet-5.5 prompt v1 | 17/19 | 98% | 100% | 99% | 138/138 (+1 inventati) | 7/7 | 2 | 2 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v2 | 17/19 | 99% | 100% | 100% | 136/138 | 7/7 | 0 | 0 | 11 (11 a vuoto) |  |  |
| sonnet-5.5-api prompt v2 | 18/19 | 99% | 100% | 100% | 137/138 | 7/7 | 0 | 0 | 9 (9 a vuoto) |  |  |

## Caso per caso (righe perfette / righe)

| caso | cosa prova | gemini-3.8-flash prompt v1 | gemini-3.8-flash prompt v2 | gemini-3.8-flash prompt v3 | gemini-pro prompt v1 | gemini-pro prompt v2 | haiku-4.5 prompt v1 | haiku-5.5 prompt v2 | haiku-5.5 prompt v3 | locale-qwen3.5-0.8b | opus-5.5 prompt v1 | opus-5.5 prompt v2 | opus-5.5-api prompt v2 | opus-5.5-api prompt v3 | sonnet-5.5 prompt v1 | sonnet-5.5 prompt v2 | sonnet-5.5-api prompt v2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| reale-01 | pagina di esempio con calligrafia vera | 1/2 ⚠ | 1/2 ⚠ | 2/2 | 2/2 | 1/2 ⚠ | 1/2 | 1/2 ⚠ | 1/2 ⚠ |  | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 ⚠ | 1/2 ⚠ | 1/2 ⚠ |
| reale-02 | pagina di esempio con calligrafia vera | 1/2 ⚠ | 1/2 ⚠ | 1/2 ⚠ | 0/2 ⚠ | 1/2 ⚠ | 0/2 ⚠ | 0/2 ⚠ | 0/2 ⚠ |  | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 ⚠ | 1/2 ⚠ | 1/2 ⚠ |
| reale-03 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 ⚠ | 0/1 ⚠ | 0/1 ⚠ |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-04 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 ⚠ | 1/1 | 1/1 |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-05 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-06 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-07 | pagina di esempio con calligrafia vera | 1/4 | 4/4 | 4/4 | 1/4 | 4/4 | 1/4 | 2/4 | 3/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 3/4 ⚠ | 3/4 ⚠ | 3/4 |
| reale-08 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-09 | pagina di esempio con calligrafia vera | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 ⚠ | 3/3 | 3/3 |  | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| reale-10 | pagina di esempio con calligrafia vera | 4/4 | 4/4 | 4/4 | 1/4 | 4/4 | 1/4 ⚠ | 1/4 | 4/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| reale-11 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-12 | pagina di esempio con calligrafia vera | 2/4 | 2/4 | 2/4 | 2/4 | 4/4 | 3/4 | 2/4 | 4/4 |  | 2/4 | 2/4 | 2/4 | 4/4 | 2/4 | 4/4 | 2/4 |
| reale-13 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |  | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-14 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 |  | 0/1 ⚠ | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| pulita-C | bolla bianca, come arrivata | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 2/4 | 4/4 | 4/4 | 0/4 ⚠ | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| pulita-P1 | bolla bianca, come arrivata | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | FALLITA | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| pulita-P2 | bolla bianca, come arrivata | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 0/15 ⚠ | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| pulita-P3 | bolla bianca, come arrivata | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 15/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 |
| sint-C-mag-penna | MAG a penna blu su ogni riga | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 0/4 | 4/4 | 4/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-C-mag-evidenziato | MAG a penna nera evidenziato in giallo/verde, sopra le taglie | 2/4 ⚠ | 4/4 | 4/4 | 1/4 ⚠ | 4/4 | 0/4 ⚠ | 3/4 | 4/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 2/4 ⚠ | 4/4 | 4/4 |
| sint-C-mag-cerchiato-matita | MAG a MATITA, cerchiato | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 | 0/4 | 3/4 | 3/4 |  | 3/4 | 3/4 | 3/4 | 3/4 | 4/4 | 3/4 | 3/4 |
| sint-C-split-taglia | una taglia divisa su due magazzini (2 MAG 1 + 1 MAG 2) | 4/4 | 4/4 | 4/4 | 2/4 ⚠ | 4/4 | 1/4 | 4/4 | 4/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-C-barrate | riga 3 cancellata con un tratto, riga 4 con X sul numero | 2/4 ⚠ | 4/4 | 4/4 | 4/4 | 4/4 | 0/4 | 4/4 | 4/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-C-qta-corretta | quantita' stampata S/5 barrata e corretta a mano in 4 | 2/4 ⚠ | 4/4 | 4/4 | 2/4 ⚠ | 4/4 | 0/4 | 4/4 | 4/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-P1-mag-ogni-riga | 11 righe fitte, MAG su ognuna | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 1/11 | 11/11 | 11/11 |  | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P1-graffe | due graffe a margine: 'M2' per le righe 1-2, 'M1' per 3-11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 0/11 | 11/11 | 11/11 |  | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P1-solo-spunte | solo spunte di controllo e 'ok 8 colli': nessun magazzino | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |  | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P1-mix | MAG su alcune righe, 2 barrate, 1 con X, spunte | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 8/11 | 11/11 | 11/11 |  | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P2-evidenziati | 15 righe, MAG evidenziato su ognuna, 2 righe barrate | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 1/15 | 15/15 | 15/15 |  | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-P2-matita | 15 righe, MAG a MATITA leggera | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 1/15 | 15/15 | 15/15 |  | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-P3-rossa-codice | 17 righe, penna rossa, nome cliente e codice aggiunti a mano | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 4/17 | 17/17 | 17/17 |  | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 |
| sint-P2-mag-di-pagina | un solo 'TUTTO MAG 2' in testa alla pagina | 1/15 | 15/15 | 15/15 | 15/15 | 15/15 | 1/15 | 15/15 | 15/15 |  | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-P3-sopra-taglie | MAG scritto SOPRA la colonna Size/Qty: copre lo stampato | 17/17 | 17/17 | 17/17 | 16/17 ⚠ | 15/17 ⚠ | 12/17 ⚠ | 16/17 | 17/17 |  | 17/17 | 17/17 | 16/17 | 17/17 | 16/17 | 17/17 | 17/17 |
| sint-P1-ruotata-90 | scansione coricata (90 gradi) con MAG | 1/11 | 9/11 | 6/11 ⚠ | 1/11 | 11/11 | 1/11 | 1/11 | 1/11 |  | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P2-capovolta | scansione capovolta (180 gradi), pulita | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 1/15 | 14/15 ⚠ | 13/15 ⚠ |  | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-C-foto-telefono | foto da telefono: storta, in ombra, sfocata, compressa | 2/4 | 2/4 | 2/4 | 2/4 | 2/4 | 0/4 ⚠ | 3/4 | 3/4 |  | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-P3-fax | bianco e nero a bassa risoluzione (fax/fotocopia) | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 4/17 ⚠ | 16/17 | 17/17 |  | 17/17 | 17/17 | 17/17 | 16/17 | 17/17 | 16/17 | 17/17 |

⚠ = almeno un errore silenzioso (non intercettato dal checksum).

- **gemini-3.8-flash prompt v1**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO. Prompt e schema v1.

- **gemini-3.8-flash prompt v2**: Via OpenRouter, API vera con output vincolato allo schema. Prompt corrente (v2). Costo MISURATO.

- **gemini-3.8-flash prompt v3**: Via OpenRouter, API vera con output vincolato allo schema. Prompt v3 (barrate sul Seq-no, MAG su riga barrata, incertezze ristrette). Costo MISURATO.

- **gemini-pro prompt v1**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO. Prompt e schema v1.

- **gemini-pro prompt v2**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO.

- **haiku-4.5 prompt v1**: Letto come sotto-agente di Claude Code, non via API: stesso prompt e schema, ma senza output vincolato e con le pagine lette in sequenza nella stessa sessione. Costo STIMATO dal listino (ragionamento escluso), non misurato.

- **haiku-5.5 prompt v2**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO.

- **haiku-5.5 prompt v3**: Via OpenRouter, API vera con output vincolato allo schema. Prompt v3 (barrate sul Seq-no, MAG su riga barrata, incertezze ristrette). Costo MISURATO.

- **locale-qwen3.5-0.8b**: Ollama su CPU (Ryzen 7 7730U, nessuna GPU)

- **opus-5.5 prompt v1**: Letto come sotto-agente di Claude Code, non via API: stesso prompt e schema, ma senza output vincolato e con le pagine lette in sequenza nella stessa sessione. Costo STIMATO dal listino (ragionamento escluso), non misurato.

- **opus-5.5 prompt v2**: Sotto-agente di Claude Code, non API. Prompt v2 (regole su magazzini, incertezze, codice a mano). Costo STIMATO dal listino, ragionamento escluso. 14 casi aggiunti il 2026-10-09 con il prompt v2 corrente (una riga in piu' sui pacchi misti).

- **opus-5.5-api prompt v2**: Via OpenRouter, API vera con output vincolato allo schema, una pagina per chiamata, ragionamento alle impostazioni predefinite. Costo MISURATO.

- **opus-5.5-api prompt v3**: Via OpenRouter, API vera con output vincolato allo schema. Prompt v3 (barrate sul Seq-no, MAG su riga barrata, incertezze ristrette). Costo MISURATO.

- **sonnet-5.5 prompt v1**: Letto come sotto-agente di Claude Code, non via API: stesso prompt e schema, ma senza output vincolato e con le pagine lette in sequenza nella stessa sessione. Costo STIMATO dal listino (ragionamento escluso), non misurato.

- **sonnet-5.5 prompt v2**: Sotto-agente di Claude Code, non API. Prompt v2 (regole su magazzini, incertezze, codice a mano). Costo STIMATO dal listino, ragionamento escluso. 14 casi aggiunti il 2026-10-09 con il prompt v2 corrente (una riga in piu' sui pacchi misti).

- **sonnet-5.5-api prompt v2**: Via OpenRouter, API vera con output vincolato allo schema, una pagina per chiamata, ragionamento alle impostazioni predefinite. Costo MISURATO.

## Errori

### gemini-3.8-flash prompt v1

- `reale-01`: riga 2 codice: atteso JD9573, letto 'DZ9573'
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '550/2 570/2'
- `reale-07`: riga 1 barrata: atteso True, letto False
- `reale-07`: riga 3 barrata: atteso True, letto False
- `reale-07`: riga 4 barrata: atteso True, letto False
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('X sul numero seq 2; MAG 1 evidenziato in verde')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-evidenziato`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '450/1 460/1 470/1 480/1 490/1 500/1 440/1 510/1'
- `sint-C-mag-evidenziato`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '450/1 460/1 470/1 480/1 490/1 500/1 440/1 510/1'
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-C-barrate`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 ST/1 LT/1 2XLT/1 XST/1 MT/1 XLT/1 4XLT/1'
- `sint-C-barrate`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 ST/1 LT/1 2XLT/1 XST/1 MT/1 XLT/1 4XLT/1'
- `sint-C-qta-corretta`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '28/1 29/1 30/1 31/1 32/1 33/1 34/1 35/1'
- `sint-C-qta-corretta`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '28/1 29/1 30/1 31/1 32/1 33/1 34/1 35/1'
- `sint-P2-mag-di-pagina`: riga 13 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 14 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 15 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 16 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 17 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 18 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 19 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 20 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 21 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 22 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 23 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 24 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 25 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 26 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 1 magazzino: atteso ['MAG 2'], letto - ('20,00 EUR 2')
- `sint-P1-ruotata-90`: riga 3 magazzino: atteso ['MAG 2'], letto - ('19,00 EUR 1')
- `sint-P1-ruotata-90`: riga 4 magazzino: atteso ['MAG 1'], letto - ('19,00 EUR 1')
- `sint-P1-ruotata-90`: riga 5 magazzino: atteso ['MAG 2'], letto - ('19,00 EUR 2')
- `sint-P1-ruotata-90`: riga 6 magazzino: atteso ['MAG 1'], letto - ('19,00 EUR 1')
- `sint-P1-ruotata-90`: riga 7 magazzino: atteso ['MAG 2'], letto - ('35,00 EUR 2')
- `sint-P1-ruotata-90`: riga 8 magazzino: atteso ['MAG 1'], letto - ('35,00 EUR 1')
- `sint-P1-ruotata-90`: riga 9 magazzino: atteso ['MAG 2'], letto - ('29,00 EUR 2')
- `sint-P1-ruotata-90`: riga 10 magazzino: atteso ['MAG 1'], letto - ('45,00 EUR 1')
- `sint-P1-ruotata-90`: riga 11 magazzino: atteso ['MAG 2'], letto - ('45,00 EUR 2')
- `sint-C-foto-telefono`: riga 1 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')

### gemini-3.8-flash prompt v2

- `reale-01`: riga 2 codice: atteso JD9573, letto 'IJ9573'
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '550/2 570/2'
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('MAG 1')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-P1-ruotata-90`: riga 2 magazzino: atteso -, letto ['MAG 2'] ('MAG 2')
- `sint-P1-ruotata-90`: riga 3 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-C-foto-telefono`: riga 1 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')

### gemini-3.8-flash prompt v3

- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '550/2 570/2'
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('MAG 1')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-P1-ruotata-90`: riga 2 magazzino: atteso -, letto ['MAG 2'] ('MAG 2')
- `sint-P1-ruotata-90`: riga 3 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-P1-ruotata-90`: riga 7 codice: atteso JZ6549, letto 'JZ2549'
- `sint-P1-ruotata-90`: riga 8 codice: atteso JZ6550, letto 'JZ2550'
- `sint-P1-ruotata-90`: riga 9 codice: atteso JZ6557, letto 'JZ2557'
- `sint-C-foto-telefono`: riga 1 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')

### gemini-pro prompt v1

- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '550/2 570/2'
- `reale-02`: riga 2 taglie: atteso '580/1 620/1 640/2', letto '560/1 620/1 640/2'
- `reale-07`: riga 1 barrata: atteso True, letto False
- `reale-07`: riga 3 barrata: atteso True, letto False
- `reale-07`: riga 4 barrata: atteso True, letto False
- `reale-10`: riga 2 barrata: atteso True, letto False
- `reale-10`: riga 3 barrata: atteso True, letto False
- `reale-10`: riga 4 barrata: atteso True, letto False
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('MAG 1')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-evidenziato`: riga 2 taglie: atteso '530/1 540/2 550/1 560/2 570/1 580/2 590/1 520/1', letto '530/1 540/2 550/1 560/2 570/1 580/2 590/1 600/1'
- `sint-C-mag-evidenziato`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '280/1 290/1 300/1 310/1 320/1 330/1 340/1 350/1'
- `sint-C-mag-evidenziato`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '280/1 290/1 300/1 310/1 320/1 330/1 340/1 350/1'
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-C-split-taglia`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '300/1 310/1 320/1 330/1 340/1 350/1 280/1 290/1'
- `sint-C-split-taglia`: riga 3 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-C-split-taglia`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '300/1 310/1 320/1 330/1 340/1 350/1 280/1 290/1'
- `sint-C-qta-corretta`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '28/1 29/1 30/1 31/1 32/1 33/1 34/1 35/1'
- `sint-C-qta-corretta`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '28/1 29/1 30/1 31/1 32/1 33/1 34/1 35/1'
- `sint-P3-sopra-taglie`: riga 29 taglie: atteso 'M/1 L/1 XL/1', letto 'M/1 L/2'
- `sint-P1-ruotata-90`: riga 1 magazzino: atteso ['MAG 2'], letto - ('20,00 EUR 2')
- `sint-P1-ruotata-90`: riga 3 magazzino: atteso ['MAG 2'], letto - ('19,00 EUR 2')
- `sint-P1-ruotata-90`: riga 4 magazzino: atteso ['MAG 1'], letto - ('19,00 EUR 1')
- `sint-P1-ruotata-90`: riga 5 magazzino: atteso ['MAG 2'], letto - ('19,00 EUR 2')
- `sint-P1-ruotata-90`: riga 6 magazzino: atteso ['MAG 1'], letto - ('19,00 EUR 1')
- `sint-P1-ruotata-90`: riga 7 magazzino: atteso ['MAG 2'], letto - ('35,00 EUR 2')
- `sint-P1-ruotata-90`: riga 8 magazzino: atteso ['MAG 1'], letto - ('35,00 EUR 2')
- `sint-P1-ruotata-90`: riga 9 magazzino: atteso ['MAG 2'], letto - ('23,00 EUR 2')
- `sint-P1-ruotata-90`: riga 10 magazzino: atteso ['MAG 1'], letto - ('45,00 EUR 1')
- `sint-P1-ruotata-90`: riga 11 magazzino: atteso ['MAG 2'], letto - ('45,00 EUR 2')
- `sint-C-foto-telefono`: riga 1 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')

### gemini-pro prompt v2

- `reale-01`: riga 2 codice: atteso JD9573, letto 'ID9573'
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '560/2 570/2'
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-P3-sopra-taglie`: riga 27 magazzino: atteso -, letto ['MAG 1'] ('MAG 1')
- `sint-P3-sopra-taglie`: riga 29 taglie: atteso 'M/1 L/1 XL/1', letto 'M/1 L/2'
- `sint-C-foto-telefono`: riga 1 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto ['MAG 2'] ('MAG 2')

### haiku-4.5 prompt v1

- `sint-C-mag-evidenziato`: riga 1 taglie: atteso 'XS/3 S/5 M/5 L/3', letto 'S/5 L/3 M/5'
- `sint-C-mag-evidenziato`: riga 2 taglie: atteso '530/1 540/2 550/1 560/2 570/1 580/2 590/1 520/1', letto '550/2 570/1 590/1 520/1'
- `sint-C-mag-evidenziato`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto 'LT2/1 XS/1 L/1 XL/1 510/4'
- `sint-C-mag-evidenziato`: riga 3 magazzino: atteso ['MAG 1'], letto - ('MAG')
- `sint-C-mag-evidenziato`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto 'LT2/1 XS/1 L/1 XL/1 510/4'
- `pulita-C`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XL/1 2XT2/1 XL/1 ST2/1 XS/1 510/1'
- `pulita-C`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XL/1 2XT2/1 XL/1 ST2/1 XS/1 510/1'
- `reale-09`: riga 1 taglie: atteso 'L/4', letto 'L/4 L/10'
- `reale-09`: riga 2 codice: atteso H44527, letto 'JN5459'
- `reale-09`: riga 2 taglie: atteso 'L/10', letto '1314/2'
- `reale-09`: riga 2 (JN5459) mancante
- `sint-P3-sopra-taglie`: riga 28 taglie: atteso 'XL/4 L/15 M/15 S/15 XS/7', letto 'XL/4 L/15 XS/7'
- `sint-P3-sopra-taglie`: riga 28 magazzino: atteso ['MAG 1'], letto - ('MAG')
- `sint-P3-sopra-taglie`: riga 29 taglie: atteso 'M/1 L/1 XL/1', letto 'M/1'
- `sint-P3-sopra-taglie`: riga 30 taglie: atteso 'XS/7 XL/4 S/15 L/15 M/15', letto 'XS/7 XL/4 L/15 M/15'
- `sint-P3-sopra-taglie`: riga 30 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-sopra-taglie`: riga 37 taglie: atteso 'XS/1 S/4 M/6 L/6 XL/4 2XL/3', letto 'XS/1 S/7 XL/4 L/12'
- `sint-P3-sopra-taglie`: riga 40 taglie: atteso '5-6A/1 7-8A/1 910A/1 1112/1 1314/1', letto '5-6A/1 6-8A/1 1112/1 1314/1'
- `sint-P3-sopra-taglie`: riga 40 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-P3-fax`: riga 27 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-fax`: riga 29 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-fax`: riga 30 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-fax`: riga 31 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-fax`: riga 32 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-fax`: riga 33 codice: atteso KA5261, letto 'KA5281'
- `sint-P3-fax`: riga 33 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-fax`: riga 34 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-fax`: riga 35 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-fax`: riga 37 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-fax`: riga 38 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-fax`: riga 40 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-fax`: riga 41 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-fax`: riga 43 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-mix`: riga 5 barrata: atteso True, letto False
- `sint-P1-mix`: riga 8 barrata: atteso True, letto False
- `sint-P1-mix`: riga 10 barrata: atteso True, letto False
- `sint-P3-rossa-codice`: riga 27 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-rossa-codice`: riga 29 magazzino: atteso ['MAG 2'], letto - ('VERONELLI')
- `sint-P3-rossa-codice`: riga 30 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-rossa-codice`: riga 31 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-rossa-codice`: riga 32 magazzino: atteso ['MAG 2'], letto - ('JN9131 x 3')
- `sint-P3-rossa-codice`: riga 33 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P3-rossa-codice`: riga 34 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-rossa-codice`: riga 35 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-rossa-codice`: riga 37 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-rossa-codice`: riga 38 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-rossa-codice`: riga 40 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-rossa-codice`: riga 41 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P3-rossa-codice`: riga 43 magazzino: atteso ['MAG 2'], letto - ('')
- `reale-01`: riga 2 barrata: atteso True, letto False
- `sint-C-foto-telefono`: riga 1 magazzino: atteso ['MAG 1'], letto - ('MAG')
- `sint-C-foto-telefono`: riga 2 magazzino: atteso ['MAG 2'], letto - ('MAG')
- `sint-C-foto-telefono`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 510/1 LT2/1 M/1'
- `sint-C-foto-telefono`: riga 3 magazzino: atteso ['MAG 2'], letto - ('MAG')
- `sint-C-foto-telefono`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 510/1 LT2/1 M/1'
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto - ('MAG')
- `sint-P2-matita`: riga 12 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-matita`: riga 13 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 14 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 15 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-matita`: riga 16 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 17 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 18 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-matita`: riga 19 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 20 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 21 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-matita`: riga 22 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 23 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-matita`: riga 24 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-matita`: riga 25 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 1 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 3 (JZ2508) mancante
- `sint-P1-ruotata-90`: riga 4 (JZ2513) mancante
- `sint-P1-ruotata-90`: riga 5 (JZ2521) mancante
- `sint-P1-ruotata-90`: riga 6 (JZ2524) mancante
- `sint-P1-ruotata-90`: riga 7 (JZ6549) mancante
- `sint-P1-ruotata-90`: riga 8 (JZ6550) mancante
- `sint-P1-ruotata-90`: riga 9 (JZ6557) mancante
- `sint-P1-ruotata-90`: riga 10 (JZ6577) mancante
- `sint-P1-ruotata-90`: riga 11 (JZ6579) mancante
- `sint-P2-capovolta`: riga 13 (JZ6586) mancante
- `sint-P2-capovolta`: riga 14 (JZ6593) mancante
- `sint-P2-capovolta`: riga 15 (JZ6607) mancante
- `sint-P2-capovolta`: riga 16 (JZ6608) mancante
- `sint-P2-capovolta`: riga 17 (JZ6611) mancante
- `sint-P2-capovolta`: riga 18 (JZ6673) mancante
- `sint-P2-capovolta`: riga 19 (JZ6675) mancante
- `sint-P2-capovolta`: riga 20 (JZ9139) mancante
- `sint-P2-capovolta`: riga 21 (JZ6676) mancante
- `sint-P2-capovolta`: riga 22 (JZ6678) mancante
- `sint-P2-capovolta`: riga 23 (JZ9138) mancante
- `sint-P2-capovolta`: riga 24 (KA5262) mancante
- `sint-P2-capovolta`: riga 25 (KB0786) mancante
- `sint-P2-capovolta`: riga 26 (KD0985) mancante
- `sint-C-barrate`: riga 1 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-barrate`: riga 2 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-barrate`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-barrate`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-barrate`: riga 4 barrata: atteso True, letto False
- `sint-C-split-taglia`: riga 2 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-split-taglia`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-split-taglia`: riga 3 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-C-split-taglia`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-split-taglia`: riga 4 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 1 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 3 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 4 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 5 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 6 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 7 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 8 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 9 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 10 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-mag-ogni-riga`: riga 11 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-qta-corretta`: riga 1 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-qta-corretta`: riga 2 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-C-qta-corretta`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-qta-corretta`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `reale-14`: riga 1 (JM9191) mancante
- `reale-03`: riga 1 taglie: atteso '8/1 9-/3 11-/1', letto '8/1 9/3 11-/1'
- `sint-P2-evidenziati`: riga 12 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-evidenziati`: riga 13 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-evidenziati`: riga 14 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-evidenziati`: riga 15 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-evidenziati`: riga 16 barrata: atteso True, letto False
- `sint-P2-evidenziati`: riga 16 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-evidenziati`: riga 17 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-evidenziati`: riga 18 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-evidenziati`: riga 19 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-evidenziati`: riga 20 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-evidenziati`: riga 21 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-evidenziati`: riga 22 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-evidenziati`: riga 23 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-evidenziati`: riga 24 barrata: atteso True, letto False
- `sint-P2-evidenziati`: riga 24 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P2-evidenziati`: riga 25 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 13 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 14 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 15 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 16 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 17 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 18 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 19 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 20 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 21 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 22 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 23 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 24 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 25 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-mag-di-pagina`: riga 26 magazzino: atteso ['MAG 2'], letto - ('')
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '8-/2 560/2'
- `reale-02`: riga 2 taglie: atteso '580/1 620/1 640/2', letto '840/1 040/1 640/2'
- `sint-C-mag-penna`: riga 1 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-penna`: riga 2 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-C-mag-penna`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-mag-penna`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-penna`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-mag-penna`: riga 4 magazzino: atteso ['MAG 2'], letto - ('')
- `reale-12`: riga 2 barrata: atteso True, letto False
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('MAG 1')
- `reale-07`: riga 1 barrata: atteso True, letto False
- `reale-07`: riga 3 barrata: atteso True, letto False
- `reale-07`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `reale-07`: riga 4 barrata: atteso True, letto False
- `reale-05`: riga 1 (F35542) mancante
- `reale-04`: riga 1 taglie: atteso '4/2 5/1 6/1 7/2', letto '4/2 S/1 6/1 7/2'
- `sint-P1-graffe`: riga 1 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-graffe`: riga 2 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-graffe`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 4 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 5 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 6 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 7 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 8 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 9 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 10 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-graffe`: riga 11 magazzino: atteso ['MAG 1'], letto - ('')
- `reale-10`: riga 2 codice: atteso KB9419, letto 'KB9417'
- `reale-10`: riga 2 taglie: atteso 'XS/1', letto ''
- `reale-10`: riga 2 barrata: atteso True, letto False
- `reale-10`: riga 3 barrata: atteso True, letto False
- `reale-10`: riga 4 taglie: atteso '7/1', letto '1/1'
- `reale-10`: riga 4 barrata: atteso True, letto False
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 2 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-mag-cerchiato-matita`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XLT/1 2XT2/1 XL/1 ST2/1 XS/1 LT2/1 M/1'
- `sint-C-mag-cerchiato-matita`: riga 4 magazzino: atteso ['MAG 1'], letto - ('')

### haiku-5.5 prompt v2

- `reale-01`: riga 2 codice: atteso JD9573, letto 'UD9573'
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '540/2 550/2'
- `reale-02`: riga 2 taglie: atteso '580/1 620/1 640/2', letto '560/1 620/1 640/2'
- `reale-03`: riga 1 taglie: atteso '8/1 9-/3 11-/1', letto '8-/1 9-/3 11-/1'
- `reale-07`: riga 3 barrata: atteso True, letto False
- `reale-07`: riga 4 barrata: atteso True, letto False
- `reale-10`: riga 2 barrata: atteso True, letto False
- `reale-10`: riga 3 barrata: atteso True, letto False
- `reale-10`: riga 4 barrata: atteso True, letto False
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('MAG 1')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-evidenziato`: riga 1 taglie: atteso 'XS/3 S/5 M/5 L/3', letto 'S/5 M/5 L/3'
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-P3-sopra-taglie`: riga 27 magazzino: atteso -, letto ['MAG 1'] ("MAG 1 scritto tra le righe 27 e 28, non e' chiaro a quale riga si riferisca")
- `sint-P1-ruotata-90`: riga 1 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 3 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 4 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 5 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 6 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 7 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 8 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 9 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 10 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 11 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-capovolta`: riga 14 codice: atteso JZ6593, letto 'JZ6693'
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto - ('MAG ?')
- `sint-P3-fax`: riga 41 magazzino: atteso ['MAG 1'], letto - ('MAG ?')

### haiku-5.5 prompt v3

- `reale-01`: riga 2 codice: atteso JD9573, letto 'UD9573'
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '550/2 580/2'
- `reale-02`: riga 2 taglie: atteso '580/1 620/1 640/2', letto '560/1 620/1 640/2'
- `reale-03`: riga 1 taglie: atteso '8/1 9-/3 11-/1', letto '8-/1 9-/3 11-/1'
- `reale-07`: riga 3 barrata: atteso True, letto False
- `reale-11`: riga 1 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `sint-P1-ruotata-90`: riga 1 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 3 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 4 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 5 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 6 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 7 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 8 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 9 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P1-ruotata-90`: riga 10 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-P1-ruotata-90`: riga 11 magazzino: atteso ['MAG 2'], letto - ('')
- `sint-P2-capovolta`: riga 14 codice: atteso JZ6593, letto 'JZ6693'
- `sint-P2-capovolta`: riga 24 taglie: atteso '5/20', letto 'S/20'
- `sint-C-foto-telefono`: riga 4 magazzino: atteso ['MAG 1'], letto - ('MAG ?')

### locale-qwen3.5-0.8b

- `pulita-C`: riga 1 codice: atteso KB8172, letto ''
- `pulita-C`: riga 1 taglie: atteso 'XS/3 S/5 M/5 L/3', letto ''
- `pulita-C`: riga 2 codice: atteso KI1676, letto ''
- `pulita-C`: riga 2 taglie: atteso '530/1 540/2 550/1 560/2 570/1 580/2 590/1 520/1', letto ''
- `pulita-C`: riga 3 codice: atteso KI1690, letto ''
- `pulita-C`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto ''
- `pulita-C`: riga 4 codice: atteso KI1690, letto ''
- `pulita-C`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto ''
- `pulita-P1`: estrazione fallita
- `pulita-P1`: riga 1 (HS9760) mancante
- `pulita-P1`: riga 2 (JZ9136) mancante
- `pulita-P1`: riga 3 (JZ2508) mancante
- `pulita-P1`: riga 4 (JZ2513) mancante
- `pulita-P1`: riga 5 (JZ2521) mancante
- `pulita-P1`: riga 6 (JZ2524) mancante
- `pulita-P1`: riga 7 (JZ6549) mancante
- `pulita-P1`: riga 8 (JZ6550) mancante
- `pulita-P1`: riga 9 (JZ6557) mancante
- `pulita-P1`: riga 10 (JZ6577) mancante
- `pulita-P1`: riga 11 (JZ6579) mancante
- `pulita-P2`: riga 12 codice: atteso JZ9138, letto ''
- `pulita-P2`: riga 12 taglie: atteso 'S/3 M/7 L/7 XL/5 2XL/4', letto 'S/3 M7 L7 XL5 2XL4'
- `pulita-P2`: riga 13 codice: atteso JZ6586, letto ''
- `pulita-P2`: riga 13 taglie: atteso 'XL/3 L/10 M/10 S/10 XS/5', letto 'XL/3 L10 M10 S10 XS5'
- `pulita-P2`: riga 14 codice: atteso JZ6593, letto ''
- `pulita-P2`: riga 14 taglie: atteso 'XL/8 L/35 M/35 S/35 XS/8', letto 'XL/8 L35 M35 S35 XS8'
- `pulita-P2`: riga 15 codice: atteso JZ6607, letto ''
- `pulita-P2`: riga 15 taglie: atteso '910A/4 1314/6 1112/6', letto '910A4 1314/6 910A4'
- `pulita-P2`: riga 16 codice: atteso JZ6608, letto ''
- `pulita-P2`: riga 16 taglie: atteso '1112/6 1314/6 910A/4', letto '910A4 1112/6 910A4'
- `pulita-P2`: riga 17 codice: atteso JZ6611, letto ''
- `pulita-P2`: riga 17 taglie: atteso '910A/4 1112/6 1314/6', letto '910A4 1112/6 1314/6'
- `pulita-P2`: riga 18 codice: atteso JZ6673, letto ''
- `pulita-P2`: riga 18 taglie: atteso '910A/4 1112/6 1314/6', letto '910A4 1112/6 1314/6'
- `pulita-P2`: riga 19 codice: atteso JZ6675, letto ''
- `pulita-P2`: riga 19 taglie: atteso 'XL/20 L/60 M/60 S/60 XS/25', letto '910A4 1112/6 1314/6'
- `pulita-P2`: riga 20 codice: atteso JZ9139, letto ''
- `pulita-P2`: riga 20 taglie: atteso 'S/1 M/2 L/2 XL/1 2XL/1', letto 'XL/20 L60 M60 S60 XS/25'
- `pulita-P2`: riga 21 codice: atteso JZ6676, letto ''
- `pulita-P2`: riga 21 taglie: atteso 'XS/10 XL/10 L/20 M/25 S/25', letto 'S/1 M2 L2 XL1 2XL1'
- `pulita-P2`: riga 22 codice: atteso JZ6678, letto ''
- `pulita-P2`: riga 22 taglie: atteso 'XL/30 L/60 M/60 S/60 XS/30', letto 'XS/10 XL/10 L20 M25 S25'
- `pulita-P2`: riga 23 codice: atteso JZ9138, letto ''
- `pulita-P2`: riga 23 taglie: atteso 'M/20 L/20 XL/8 S/20 XS/8', letto 'XL/30 L60 M60 S60 XS/30'
- `pulita-P2`: riga 24 codice: atteso KA5262, letto ''
- `pulita-P2`: riga 24 taglie: atteso '5/20', letto 'M/20 L20 XL8 S/20 XS/8'
- `pulita-P2`: riga 25 codice: atteso KB0786, letto ''
- `pulita-P2`: riga 25 taglie: atteso 'NS/15', letto '5/20'
- `pulita-P2`: riga 26 codice: atteso KD0985, letto ''
- `pulita-P2`: riga 26 taglie: atteso 'XS/13 XL/12 S/30 L/30 M/30', letto 'NS/15'
- `pulita-P3`: riga 28 taglie: atteso 'XL/4 L/15 M/15 S/15 XS/7', letto 'XS/7'
- `pulita-P3`: riga 39 taglie: atteso 'NS/5', letto 'S/2 M/3 L/2 XL/2'

### opus-5.5 prompt v1

- `reale-14`: riga 1 codice: atteso JM9191, letto 'JN9131'
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('X a penna sul numero di riga 2; MAG 1 (evidenziato verde)')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1 (cerchiato a matita; cifra sovrapposta al prezzo, lettura incerta)')

### opus-5.5 prompt v2

- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ("MAG 1 (scritto all'altezza di questa riga; numero di riga cancellato con una X)")
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto - ('MAG ? (a matita, cerchiato, sopra il prezzo)')

### opus-5.5-api prompt v2

- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('MAG 1 (evidenziato, scritto sulla riga 2 barrata, appena sopra la riga 3)')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto - ('MAG ?')
- `sint-P3-sopra-taglie`: riga 27 magazzino: atteso -, letto ['MAG 1'] ('MAG 1 (scritto a cavallo tra riga 27 e riga 28, potrebbe riferirsi a una sola delle due)')

### opus-5.5-api prompt v3

- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto - ('MAG ?')
- `sint-P3-fax`: riga 41 magazzino: atteso ['MAG 1'], letto - ('MAG ?')

### sonnet-5.5 prompt v1

- `sint-C-mag-evidenziato`: riga 3 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XT2/1 ST2/1 2XT2/1 XS/L/1 XL/L/1 510/1 LT2/1 M/L/1'
- `sint-C-mag-evidenziato`: riga 4 taglie: atteso '3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1', letto '3XT2/1 ST2/1 2XT2/1 XS/L/1 XL/L/1 510/1 LT2/1 M/L/1'
- `sint-P3-sopra-taglie`: riga 27 magazzino: atteso -, letto ['MAG 1'] ('MAG 1 (parzialmente sovrapposto, tra le righe 27 e 28)')
- `reale-01`: riga 2 codice: atteso JD9573, letto 'UD9573'
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '530/2 560/2'
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('numero seq 2 cancellato con una X a penna; MAG 1 (evidenziato verde)')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `reale-07`: riga 4 codice: atteso JZ6878, letto 'JZ6578'

### sonnet-5.5 prompt v2

- `reale-01`: riga 2 codice: atteso JD9573, letto 'UD9573'
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto ['MAG 1'] ('MAG 1')
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '530/2 560/2'
- `reale-07`: riga 4 codice: atteso JZ6878, letto 'JZ6578'
- `sint-P3-fax`: riga 41 magazzino: atteso ['MAG 1'], letto - ('MAG ? (cifra non distinguibile, 1 o 2)')

### sonnet-5.5-api prompt v2

- `reale-01`: riga 2 codice: atteso JD9573, letto 'UD9573'
- `reale-02`: riga 1 taglie: atteso '550/2 560/2', letto '530/2 560/2'
- `reale-07`: riga 3 magazzino: atteso ['MAG 1'], letto - ('TAG 1 scritto a mano e barrato')
- `reale-12`: riga 2 magazzino: atteso -, letto ['MAG 1'] ('MAG 1 (scritto sulla riga barrata)')
- `reale-12`: riga 3 magazzino: atteso ['MAG 1'], letto - ('')
- `sint-C-mag-cerchiato-matita`: riga 1 magazzino: atteso ['MAG 2'], letto - ('MAG ?')
