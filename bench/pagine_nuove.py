"""Trascrizione di riferimento delle bolle pulite in `altrebolle/`.

Ogni riga e' (seq, codice, descrizione, colore, totale, size_qty). Le coordinate
(`y` delle righe e `x` delle colonne, in pixel a 200 dpi) servono solo al
generatore di varianti, per sapere dove "scrivere a penna".

Attenzione ai nomi dei file: l'ordine alfabetico NON e' l'ordine delle pagine
(…14291 e' pagina 1, …14290 e' pagina 2).
"""
from __future__ import annotations

PAGINE = {
    "C": {
        "file": "SKM_C451i26100210330.pdf",
        "tipo_documento": "CONSOLIDATED ORDER NUMBER",
        "numero_documento": "26BN262785",
        "data_documento": "11.09.26",
        "warehouse": "Spain-50700 CAS",
        # 101 colli dichiarati ma solo 43 in questa pagina: e' "Page 1" di una
        # bolla il cui seguito non e' stato scansionato.
        "total_pieces": 101,
        "continua": False,
        "x": {"sx": 120, "nome": 480, "taglie": (890, 1350), "prezzo": (1355, 1528), "dx": 1530},
        "righe": [
            ("1", "KB8172", "W ENERGIZE TS", "CRLI", 16, "XS/3 S/5 M/5 L/3", 1178),
            ("2", "KI1676", "GALAXY 8 J", "NTGREY/TEGRME/SCRGRN", 11,
             "530/1 540/2 550/1 560/2 570/1 580/2 590/1 520/1", 1372),
            ("3", "KI1690", "GALAXY 8 EL C", "NTGREY/TEGRME/SCRGRN", 8,
             "3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1", 1592),
            ("4", "KI1690", "GALAXY 8 EL C", "NTGREY/TEGRME/SCRGRN", 8,
             "3XLT/1 ST2/1 LT2/1 2XT2/1 XS/L/1 M/L/1 XL/L/1 510/1", 1917),
        ],
    },
    "P1": {
        "file": "SKM_C451i26100514291.pdf",
        "tipo_documento": "DELIVERY NOTE",
        "numero_documento": "3000342857",
        "data_documento": "22.09.26",
        "warehouse": "46100 adidas Campus South",
        "total_pieces": 0,
        "continua": False,
        "x": {"sx": 68, "nome": 480, "taglie": (1110, 1388), "prezzo": (1395, 1585), "dx": 1588},
        "righe": [
            ("1", "HS9760", "TIRO L GLOVES", "BLACK/WHITE", 10, "S/3 M/4 L/3", 1149),
            ("2", "JZ9136", "ENT26 SW PNTY", "BLACK/WHITE", 5,
             "5-6A/1 7-8A/1 910A/1 1112/1 1314/1", 1186),
            ("3", "JZ2508", "ENT26 JSY", "WHITE/BLACK", 40, "XS/5 XL/5 L/10 M/10 S/10", 1453),
            ("4", "JZ2513", "ENT26 SHO", "TENABL/WHITE", 200, "L/50 XL/20 M/50 S/50 XS/30", 1522),
            ("5", "JZ2521", "ENT26 SHO", "BLACK/WHITE", 40, "XS/5 S/10 M/10 L/10 XL/5", 1592),
            ("6", "JZ2524", "ENT26 JSY Y", "BLACK/WHITE", 16, "1314/6 1112/6 910A/4", 1662),
            ("7", "JZ6549", "ENT26 TR PNT Y", "TENABL/WHITE", 16, "910A/4 1314/6 1112/6", 1732),
            ("8", "JZ6550", "ENT26 TR PNT Y", "BLACK/WHITE", 16, "1314/6 1112/6 910A/4", 1802),
            ("9", "JZ6557", "ENT26 TR SHO", "TENABL/WHITE", 115, "XS/13 XL/12 S/30 L/30 M/30", 1872),
            ("10", "JZ6577", "ENT26 HOODY", "BLACK/WHITE", 40, "XL/5 L/10 M/10 S/10 XS/5", 1941),
            ("11", "JZ6579", "ENT26 HOODY", "WHITE/BLACK", 40, "XL/5 XS/5 S/10 M/10 L/10", 2011),
        ],
    },
    "P2": {
        "file": "SKM_C451i26100514290.pdf",
        "tipo_documento": "DELIVERY NOTE",
        "numero_documento": "3000342857",
        "data_documento": "",
        "warehouse": "",
        "total_pieces": 0,
        "continua": True,
        "x": {"sx": 45, "nome": 460, "taglie": (1088, 1365), "prezzo": (1372, 1552), "dx": 1556},
        "righe": [
            ("12", "JZ9138", "ENT26 SW PNT", "BLACK/WHITE", 26, "S/3 M/7 L/7 XL/5 2XL/4", 467),
            ("13", "JZ6586", "ENT26 TK JKT", "TEPORE/WHITE", 38, "XL/3 L/10 M/10 S/10 XS/5", 734),
            ("14", "JZ6593", "ENT26 TK JKT", "ROYBLU/WHITE", 121, "XL/8 L/35 M/35 S/35 XS/8", 804),
            ("15", "JZ6607", "ENT26 TK JKTY", "ROYBLU/WHITE", 16, "910A/4 1314/6 1112/6", 873),
            ("16", "JZ6608", "ENT26 TK JKTY", "BLACK/WHITE", 16, "1112/6 1314/6 910A/4", 942),
            ("17", "JZ6611", "ENT26 TK JKTY", "TENABL/WHITE", 16, "910A/4 1112/6 1314/6", 1011),
            ("18", "JZ6673", "ENT26 TEE Y", "TENABL/WHITE", 16, "910A/4 1112/6 1314/6", 1081),
            ("19", "JZ6675", "ENT26 TEE", "BLACK/WHITE", 225, "XL/20 L/60 M/60 S/60 XS/25", 1151),
            ("20", "JZ9139", "ENT26 SW PNT", "TMLGGR/WHITE", 7, "S/1 M/2 L/2 XL/1 2XL/1", 1414),
            ("21", "JZ6676", "ENT26 TEE", "TEPORE/WHITE", 90, "XS/10 XL/10 L/20 M/25 S/25", 1681),
            ("22", "JZ6678", "ENT26 TEE", "TENABL/WHITE", 240, "XL/30 L/60 M/60 S/60 XS/30", 1750),
            ("23", "JZ9138", "ENT26 SW PNT", "BLACK/WHITE", 76, "M/20 L/20 XL/8 S/20 XS/8", 1820),
            ("24", "KA5262", "TIRO LGE", "WHITE/CONAVY/BRBLUE/", 20, "5/20", 1889),
            ("25", "KB0786", "TIRO DUFFLE M", "BLACK/WHITE", 15, "NS/15", 1959),
            ("26", "KD0985", "ENT26 TR SHO", "BLACK/WHITE", 115, "XS/13 XL/12 S/30 L/30 M/30", 1997),
        ],
    },
    "P3": {
        "file": "SKM_C451i26100514301.pdf",
        "tipo_documento": "DELIVERY NOTE",
        "numero_documento": "3000342857",
        "data_documento": "",
        "warehouse": "",
        "total_pieces": 0,
        "continua": True,
        "x": {"sx": 42, "nome": 460, "taglie": (1090, 1372), "prezzo": (1378, 1558), "dx": 1562},
        "righe": [
            ("27", "KD4242", "TIRO DUFFLE L", "TENABL/WHITE", 40, "NS/40", 262),
            ("28", "KQ9071", "ENT26 MULTI JKT", "TENABL", 56, "XL/4 L/15 M/15 S/15 XS/7", 300),
            ("29", "JZ9141", "ENT26 LJKT", "BLACK/WHITE", 3, "M/1 L/1 XL/1", 567),
            ("30", "KV5397", "ENT26 MULTI JKT", "ROYBLU/WHITE", 56, "XS/7 XL/4 S/15 L/15 M/15", 802),
            ("31", "KD4245", "TIRO GYMSACK", "TENABL/WHITE", 4, "NS/4", 1069),
            ("32", "KD4245", "TIRO GYMSACK", "TENABL/WHITE", 5, "NS/5", 1302),
            ("33", "KA5261", "TIRO LGE", "ROYBLU/BLACK/WHITE", 2, "5/2", 1537),
            ("34", "KA5263", "TIRO LGE", "WHITE/BLACK/LUCRED", 2, "5/2", 1606),
            ("35", "KB0786", "TIRO DUFFLE M", "BLACK/WHITE", 2, "NS/2", 1676),
            ("36", "KD4245", "TIRO GYMSACK", "TENABL/WHITE", 3, "NS/3", 1713),
            ("37", "KF5945", "ENT26 FZ HOOD", "BLACK/WHITE", 24, "XS/1 S/4 M/6 L/6 XL/4 2XL/3", 1750),
            ("38", "KF5947", "ENT26 FZ HOOD", "TMLGGR/WHITE", 9, "S/2 M/3 L/2 XL/2", 1820),
            ("39", "JY7971", "TIRO BACKPACK", "BLACK/WHITE", 5, "NS/5", 1858),
            ("40", "KH1782", "ENT26 FZ HOOD Y", "BLACK/WHITE", 5,
             "5-6A/1 7-8A/1 910A/1 1112/1 1314/1", 1896),
            ("41", "JZ4109", "TIRO26 WIN JKT", "BLACK/WHITE", 3, "M/1 L/1 XL/1", 1965),
            ("42", "JY7992", "TIRO GYMSACK", "BLACK/WHITE", 3, "NS/3", 2002),
            ("43", "HS9765", "TIRO L WOOLIE", "BLACK/WHITE", 10, "OSFM/10", 2040),
        ],
    },
}


def scomponi(size_qty: str) -> list[tuple[str, int]]:
    """Token grezzi: `XS/L/1` e' UN pacco (una XS + una L), conta 1 nel Total."""
    coppie = []
    for token in size_qty.split():
        taglia, qta = token.rsplit("/", 1)
        coppie.append((taglia, int(qta)))
    return coppie


def pagina_attesa(chiave: str) -> dict:
    """La pagina pulita nel formato di `PaginaEstratta`."""
    p = PAGINE[chiave]
    righe = []
    for seq, codice, descrizione, colore, totale, size_qty, _y in p["righe"]:
        coppie = scomponi(size_qty)
        assert sum(q for _, q in coppie) == totale, (chiave, seq)
        righe.append(
            {
                "seq": seq,
                "codice_articolo": codice,
                "descrizione": descrizione,
                "colore": colore,
                "totale_dichiarato": totale,
                "size_qty_raw": size_qty,
                "taglie": [{"taglia": t, "qta": q} for t, q in coppie],
                "barrata": False,
                "annotazioni_manoscritte": "",
            }
        )
    return {
        "tipo_documento": p["tipo_documento"],
        "numero_documento": p["numero_documento"],
        "data_documento": p["data_documento"],
        "warehouse": p["warehouse"],
        "total_pieces_dichiarato": p["total_pieces"],
        "rotazione_gradi": 0,
        "continua_da_pagina_precedente": p["continua"],
        "righe": righe,
    }
