# Confronto modelli sul banco di prova

37 casi, 268 righe di bolla. Generato da `python bench/report.py`.

## Complessivo

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 26/37 | 85% | 100% | 97% | 127/155 (+1 inventati) | 12/15 | 8 | 8 | 0 (0 a vuoto) | $0.0167 | 32 |
| gemini-3.8-flash prompt v2 | 31/37 | 97% | 100% | 100% | 150/155 (+2 inventati) | 15/15 | 2 | 1 | 2 (1 a vuoto) | $0.0159 | 27 |
| gemini-pro prompt v1 | 26/37 | 88% | 100% | 96% | 140/155 (+1 inventati) | 9/15 | 10 | 10 | 0 (0 a vuoto) | $0.0589 | 38 |
| gemini-pro prompt v2 | 32/37 | 97% | 100% | 99% | 152/155 (+1 inventati) | 15/15 | 3 | 0 | 11 (8 a vuoto) | $0.0691 | 41 |
| haiku-5.5 prompt v2 | 24/37 | 90% | 99% | 99% | 141/155 (+2 inventati) | 10/15 | 5 | 1 | 49 (45 a vuoto) | $0.0025 | 15 |
| opus-5.5 prompt v1 | 34/37 | 99% | 100% | 100% | 153/155 (+1 inventati) | 15/15 | 1 | 1 | 0 (0 a vuoto) | $0.0355 | n.d. |
| opus-5.5 prompt v2 | 35/37 | 99% | 100% | 100% | 153/155 (+1 inventati) | 15/15 | 0 | 0 | 41 (41 a vuoto) | $0.0386 | n.d. |
| opus-5.5-api prompt v2 | 34/37 | 99% | 100% | 100% | 153/155 (+2 inventati) | 15/15 | 0 | 0 | 21 (21 a vuoto) | $0.0699 | 24 |
| sonnet-5.5 prompt v1 | 31/37 | 97% | 99% | 99% | 154/155 (+2 inventati) | 15/15 | 5 | 5 | 0 (0 a vuoto) | $0.0176 | n.d. |
| sonnet-5.5 prompt v2 | 32/37 | 98% | 99% | 100% | 153/155 | 15/15 | 3 | 0 | 24 (21 a vuoto) | $0.0188 | n.d. |

## Calligrafia vera (14 pagine di esempio)

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 10/14 | 74% | 96% | 96% | 16/17 (+1 inventati) | 5/8 | 2 | 2 | 0 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v2 | 11/14 | 85% | 96% | 96% | 16/17 (+1 inventati) | 8/8 | 2 | 1 | 1 (0 a vuoto) |  |  |
| gemini-pro prompt v1 | 10/14 | 63% | 100% | 93% | 16/17 (+1 inventati) | 2/8 | 2 | 2 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v2 | 12/14 | 93% | 96% | 96% | 17/17 | 8/8 | 2 | 0 | 3 (1 a vuoto) |  |  |
| haiku-5.5 prompt v2 | 8/14 | 59% | 96% | 89% | 16/17 (+1 inventati) | 3/8 | 4 | 0 | 16 (12 a vuoto) |  |  |
| opus-5.5 prompt v1 | 12/14 | 89% | 96% | 100% | 16/17 (+1 inventati) | 8/8 | 1 | 1 | 0 (0 a vuoto) |  |  |
| opus-5.5 prompt v2 | 13/14 | 93% | 100% | 100% | 16/17 (+1 inventati) | 8/8 | 0 | 0 | 15 (15 a vuoto) |  |  |
| opus-5.5-api prompt v2 | 13/14 | 93% | 100% | 100% | 16/17 (+1 inventati) | 8/8 | 0 | 0 | 9 (9 a vuoto) |  |  |
| sonnet-5.5 prompt v1 | 10/14 | 81% | 93% | 96% | 16/17 (+1 inventati) | 8/8 | 3 | 3 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v2 | 11/14 | 89% | 93% | 96% | 17/17 | 8/8 | 3 | 0 | 13 (10 a vuoto) |  |  |

## Bolle bianche (altrebolle/)

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| haiku-5.5 prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 5 (5 a vuoto) |  |  |
| opus-5.5 prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| opus-5.5 prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| opus-5.5-api prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v1 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v2 | 4/4 | 100% | 100% | 100% | 0/0 | 0/0 | 0 | 0 | 0 (0 a vuoto) |  |  |

## Varianti con annotazioni disegnate

| modello | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.8-flash prompt v1 | 12/19 | 83% | 100% | 97% | 111/138 | 7/7 | 6 | 6 | 0 (0 a vuoto) |  |  |
| gemini-3.8-flash prompt v2 | 16/19 | 97% | 100% | 100% | 134/138 (+1 inventati) | 7/7 | 0 | 0 | 1 (1 a vuoto) |  |  |
| gemini-pro prompt v1 | 12/19 | 89% | 100% | 96% | 124/138 | 7/7 | 8 | 8 | 0 (0 a vuoto) |  |  |
| gemini-pro prompt v2 | 16/19 | 97% | 100% | 99% | 135/138 (+1 inventati) | 7/7 | 1 | 0 | 8 (7 a vuoto) |  |  |
| haiku-5.5 prompt v2 | 12/19 | 92% | 99% | 99% | 125/138 (+1 inventati) | 7/7 | 1 | 1 | 28 (28 a vuoto) |  |  |
| opus-5.5 prompt v1 | 18/19 | 99% | 100% | 100% | 137/138 | 7/7 | 0 | 0 | 0 (0 a vuoto) |  |  |
| opus-5.5 prompt v2 | 18/19 | 99% | 100% | 100% | 137/138 | 7/7 | 0 | 0 | 26 (26 a vuoto) |  |  |
| opus-5.5-api prompt v2 | 17/19 | 99% | 100% | 100% | 137/138 (+1 inventati) | 7/7 | 0 | 0 | 12 (12 a vuoto) |  |  |
| sonnet-5.5 prompt v1 | 17/19 | 98% | 100% | 99% | 138/138 (+1 inventati) | 7/7 | 2 | 2 | 0 (0 a vuoto) |  |  |
| sonnet-5.5 prompt v2 | 17/19 | 99% | 100% | 100% | 136/138 | 7/7 | 0 | 0 | 11 (11 a vuoto) |  |  |

## Caso per caso (righe perfette / righe)

| caso | cosa prova | gemini-3.8-flash prompt v1 | gemini-3.8-flash prompt v2 | gemini-pro prompt v1 | gemini-pro prompt v2 | haiku-5.5 prompt v2 | opus-5.5 prompt v1 | opus-5.5 prompt v2 | opus-5.5-api prompt v2 | sonnet-5.5 prompt v1 | sonnet-5.5 prompt v2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| reale-01 | pagina di esempio con calligrafia vera | 1/2 ⚠ | 1/2 ⚠ | 2/2 | 1/2 ⚠ | 1/2 ⚠ | 2/2 | 2/2 | 2/2 | 1/2 ⚠ | 1/2 ⚠ |
| reale-02 | pagina di esempio con calligrafia vera | 1/2 ⚠ | 1/2 ⚠ | 0/2 ⚠ | 1/2 ⚠ | 0/2 ⚠ | 2/2 | 2/2 | 2/2 | 1/2 ⚠ | 1/2 ⚠ |
| reale-03 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 ⚠ | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-04 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-05 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-06 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-07 | pagina di esempio con calligrafia vera | 1/4 | 4/4 | 1/4 | 4/4 | 2/4 | 4/4 | 4/4 | 4/4 | 3/4 ⚠ | 3/4 ⚠ |
| reale-08 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-09 | pagina di esempio con calligrafia vera | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| reale-10 | pagina di esempio con calligrafia vera | 4/4 | 4/4 | 1/4 | 4/4 | 1/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| reale-11 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-12 | pagina di esempio con calligrafia vera | 2/4 | 2/4 | 2/4 | 4/4 | 2/4 | 2/4 | 2/4 | 2/4 | 2/4 | 4/4 |
| reale-13 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| reale-14 | pagina di esempio con calligrafia vera | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 ⚠ | 1/1 | 1/1 | 1/1 | 1/1 |
| pulita-C | bolla bianca, come arrivata | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| pulita-P1 | bolla bianca, come arrivata | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| pulita-P2 | bolla bianca, come arrivata | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| pulita-P3 | bolla bianca, come arrivata | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 |
| sint-C-mag-penna | MAG a penna blu su ogni riga | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-C-mag-evidenziato | MAG a penna nera evidenziato in giallo/verde, sopra le taglie | 2/4 ⚠ | 4/4 | 1/4 ⚠ | 4/4 | 3/4 | 4/4 | 4/4 | 4/4 | 2/4 ⚠ | 4/4 |
| sint-C-mag-cerchiato-matita | MAG a MATITA, cerchiato | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 | 3/4 | 4/4 | 3/4 |
| sint-C-split-taglia | una taglia divisa su due magazzini (2 MAG 1 + 1 MAG 2) | 4/4 | 4/4 | 2/4 ⚠ | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-C-barrate | riga 3 cancellata con un tratto, riga 4 con X sul numero | 2/4 ⚠ | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-C-qta-corretta | quantita' stampata S/5 barrata e corretta a mano in 4 | 2/4 ⚠ | 4/4 | 2/4 ⚠ | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-P1-mag-ogni-riga | 11 righe fitte, MAG su ognuna | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P1-graffe | due graffe a margine: 'M2' per le righe 1-2, 'M1' per 3-11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P1-solo-spunte | solo spunte di controllo e 'ok 8 colli': nessun magazzino | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P1-mix | MAG su alcune righe, 2 barrate, 1 con X, spunte | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P2-evidenziati | 15 righe, MAG evidenziato su ognuna, 2 righe barrate | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-P2-matita | 15 righe, MAG a MATITA leggera | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-P3-rossa-codice | 17 righe, penna rossa, nome cliente e codice aggiunti a mano | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 | 17/17 |
| sint-P2-mag-di-pagina | un solo 'TUTTO MAG 2' in testa alla pagina | 1/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-P3-sopra-taglie | MAG scritto SOPRA la colonna Size/Qty: copre lo stampato | 17/17 | 17/17 | 16/17 ⚠ | 15/17 ⚠ | 16/17 | 17/17 | 17/17 | 16/17 | 16/17 | 17/17 |
| sint-P1-ruotata-90 | scansione coricata (90 gradi) con MAG | 1/11 | 9/11 | 1/11 | 11/11 | 1/11 | 11/11 | 11/11 | 11/11 | 11/11 | 11/11 |
| sint-P2-capovolta | scansione capovolta (180 gradi), pulita | 15/15 | 15/15 | 15/15 | 15/15 | 14/15 ⚠ | 15/15 | 15/15 | 15/15 | 15/15 | 15/15 |
| sint-C-foto-telefono | foto da telefono: storta, in ombra, sfocata, compressa | 2/4 | 2/4 | 2/4 | 2/4 | 3/4 | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| sint-P3-fax | bianco e nero a bassa risoluzione (fax/fotocopia) | 17/17 | 17/17 | 17/17 | 17/17 | 16/17 | 17/17 | 17/17 | 17/17 | 17/17 | 16/17 |

⚠ = almeno un errore silenzioso (non intercettato dal checksum).

- **gemini-3.8-flash prompt v1**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO. Prompt e schema v1.

- **gemini-3.8-flash prompt v2**: Via OpenRouter, API vera con output vincolato allo schema. Prompt corrente (v2). Costo MISURATO.

- **gemini-pro prompt v1**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO. Prompt e schema v1.

- **gemini-pro prompt v2**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO.

- **haiku-5.5 prompt v2**: Via OpenRouter, API vera con output vincolato allo schema. Costo MISURATO.

- **opus-5.5 prompt v1**: Letto come sotto-agente di Claude Code, non via API: stesso prompt e schema, ma senza output vincolato e con le pagine lette in sequenza nella stessa sessione. Costo STIMATO dal listino (ragionamento escluso), non misurato.

- **opus-5.5 prompt v2**: Sotto-agente di Claude Code, non API. Prompt v2 (regole su magazzini, incertezze, codice a mano). Costo STIMATO dal listino, ragionamento escluso. 14 casi aggiunti il 2026-10-09 con il prompt v2 corrente (una riga in piu' sui pacchi misti).

- **opus-5.5-api prompt v2**: Via OpenRouter, API vera con output vincolato allo schema, una pagina per chiamata, ragionamento alle impostazioni predefinite. Costo MISURATO.

- **sonnet-5.5 prompt v1**: Letto come sotto-agente di Claude Code, non via API: stesso prompt e schema, ma senza output vincolato e con le pagine lette in sequenza nella stessa sessione. Costo STIMATO dal listino (ragionamento escluso), non misurato.

- **sonnet-5.5 prompt v2**: Sotto-agente di Claude Code, non API. Prompt v2 (regole su magazzini, incertezze, codice a mano). Costo STIMATO dal listino, ragionamento escluso. 14 casi aggiunti il 2026-10-09 con il prompt v2 corrente (una riga in piu' sui pacchi misti).

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

## I due prompt

Con il v1 lo schema di uscita non ha i campi `incertezze`, `codice_manoscritto`, `magazzino_pagina` e `note_pagina` (`bench/schema_v1.json`); il v2 e' quello dell'applicazione (`bolle/extract.py`, `bolle/schema.py`).

### Prompt v1

```text
Sei un assistente che digitalizza bolle di consegna cartacee scansionate.
Il fornitore e' sempre adidas, il destinatario sempre Jute Sport SRL.

Estrai SOLO quello che e' STAMPATO. Le scritte a mano non vanno mai usate per
correggere i dati stampati: vanno trascritte a parte nel campo
`annotazioni_manoscritte`, e sara' un operatore a decidere. Questa separazione e'
la regola piu' importante: un dato stampato che sostituisci con la tua lettura di
una calligrafia diventa un errore che finisce dritto in magazzino.

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
   sta in "Article Number" e le quantita' in una "Size Table" verticale con
   colonne Sourcing size | Size IT | Qty. Trattalo come UNA riga sola, usando la
   colonna "Size IT" come taglia, e ricostruisci `size_qty_raw` nel formato
   compatto (es. "XS/2 S/2 M/3").

COLONNA Size/Qty
E' una sequenza di token `TAGLIA/QUANTITA` separati da spazi. La taglia va
copiata ESATTAMENTE come stampata, senza interpretarla:
  8-/2                 mezza taglia calzatura, il trattino fa parte della taglia
  9-/3 11-/1           piu' taglie sulla stessa riga
  XS/2 S/7 M/10 L/8    abbigliamento
  XS/183 XL/50         quantita' a tre cifre
  NS/5                 taglia unica
  7-8A/6 910A/5 1112/5 taglie bambino
  540/3 560/6          codici numerici calzatura
Il campo `Total` di riga deve corrispondere alla somma delle quantita': se non
torna, ricontrolla la lettura prima di rispondere.

ANNOTAZIONI A MANO DA SEGNALARE
- "MAG 1" / "MAG 2" (spesso evidenziati): copiali in `annotazioni_manoscritte`.
  Se sono riferiti a una singola taglia, scrivi a quale, es.
  "9-: 1 pezzo MAG 2, 2 pezzi MAG 1".
- riga cancellata con un tratto di penna o una X: metti `barrata` a true, ma
  estrai comunque tutti i dati stampati della riga.
- quantita' o taglie corrette a penna: lascia il valore STAMPATO nei campi dati e
  annota la correzione, es. "qta XS corretta a mano da 6 a 5".
- codici articolo aggiunti a mano: mettili in `annotazioni_manoscritte`, non
  inventare una riga.

ALTRE REGOLE
- Se un valore non e' leggibile usa "" per le stringhe e 0 per i numeri. Non
  inventare mai un codice articolo.
- `rotazione_gradi`: di quanto va ruotata l'immagine in senso orario per
  raddrizzarla (0, 90, 180, 270).
- Le scritte a penna possono coprire il testo stampato: leggi sotto se ci riesci,
  altrimenti lascia il campo vuoto e segnalalo nelle annotazioni.
```

### Prompt v2

```text
Sei un assistente che digitalizza bolle di consegna cartacee scansionate.
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
  raddrizzarla (0, 90, 180, 270).
```
