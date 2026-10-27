"""Parsing della colonna Size/Qty e normalizzazione delle varianti.

La colonna `Size/Qty` delle bolle adidas e' una sequenza di token
`TAGLIA/QUANTITA` separati da spazi. Esempi reali osservati:

    8-/2                      calzatura, mezza taglia
    9-/3 11-/1                piu' taglie sulla stessa riga
    XS/2 S/7 M/10 L/8         abbigliamento
    XS/183 XL/50              quantita' a tre cifre
    NS/5                      "no size" (taglia unica)
    7-8A/6 910A/5 1112/5      taglie bambino in anni
    540/3 560/6               codici numerici calzatura
    L/4                       singola
    S/XL/1                    pacco misto: 1 pacco con dentro una S e una XL

Un token con piu' barre NON e' una taglia "S/XL": e' un pacco che contiene
un capo per ciascuna taglia elencata. Viene esploso in una riga per taglia
(S/1 e XL/1), ma nel `Total` di riga il pacco conta una volta sola.

Il totale di riga stampato in colonna `Total` e' un checksum gratuito:
se `sum(qta) != totale` l'estrazione va rivista dall'operatore.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from .config import CONFIG_DIR

# Un token e' TAGLIA/QUANTITA. La taglia puo' contenere lettere, cifre,
# trattini, '+' e anche altre barre: `S/XL/1` e' UN pacco con una S e una XL;
# la quantita' e' l'ultimo gruppo di cifre dopo l'ultimo '/'.
_TOKEN = re.compile(r"^(?P<taglia>[A-Za-z0-9][A-Za-z0-9\-\+\./]*)/(?P<qta>\d+)$")

# Taglia bambino espressa in anni: 910A = 9-10 anni, 1112 = 11-12, 7-8A = 7-8.
_ANNI_COMPATTO = re.compile(r"^(?P<a>\d{1,2})(?P<b>\d{2})A?$")
# Mezza taglia calzatura: "8-" = 8 e mezzo (DA CONFERMARE con il gestionale).
_MEZZA_TAGLIA = re.compile(r"^(?P<n>\d{1,2})-$")


@dataclass(frozen=True)
class TagliaQta:
    taglia: str
    qta: int
    # Taglie del pacco misto da cui viene questa riga ("S/XL"), "" se sciolta.
    pacco: str = ""


def espandi(taglia: str, qta: int) -> list[TagliaQta]:
    """`S/XL` in quantita' 2 -> S/2 e XL/2: due pacchi, ognuno con una S e una XL."""
    t = taglia.strip().upper()
    parti = [p for p in t.split("/") if p]
    if len(parti) < 2:
        return [TagliaQta(t, qta)]
    return [TagliaQta(p, qta, pacco="/".join(parti)) for p in parti]


def colli(taglie: list[TagliaQta]) -> Fraction:
    """Quantita' come la conta il `Total` di riga: un pacco misto vale uno."""
    return sum(
        (Fraction(t.qta, len(t.pacco.split("/"))) if t.pacco else Fraction(t.qta)
         for t in taglie),
        Fraction(0),
    )


def parse_size_qty(raw: str) -> tuple[list[TagliaQta], list[str]]:
    """Scompone la stringa Size/Qty. Ritorna (taglie, problemi)."""
    problemi: list[str] = []
    taglie: list[TagliaQta] = []
    if not raw or not raw.strip():
        return taglie, ["colonna Size/Qty vuota"]

    # Le scansioni a volte spezzano il campo su piu' righe.
    for token in raw.replace("\n", " ").split():
        m = _TOKEN.match(token)
        if not m:
            problemi.append(f"token non interpretabile: {token!r}")
            continue
        qta = int(m.group("qta"))
        if qta <= 0:
            problemi.append(f"quantita' non valida in {token!r}")
            continue
        taglie.extend(espandi(m.group("taglia"), qta))

    if not taglie:
        problemi.append(f"nessuna coppia taglia/quantita' estratta da {raw!r}")
    return taglie, problemi


def verifica_totale(taglie: list[TagliaQta], totale_dichiarato: int) -> list[str]:
    """Confronta la somma delle quantita' con il totale stampato di riga."""
    if totale_dichiarato <= 0:
        return []
    somma = colli(taglie)
    if somma != totale_dichiarato:
        return [f"somma quantita' {somma} != Total stampato {totale_dichiarato}"]
    return []


# ---------------------------------------------------------------------------
# Mappa taglia bolla -> variante gestionale
# ---------------------------------------------------------------------------
# Questa e' LA domanda aperta del progetto: nessuno dei documenti dice come
# il gestionale codifica la variante. Finche' non arriva la risposta la mappa
# vive in un CSV che l'azienda puo' compilare senza toccare il codice; tutto
# cio' che non e' mappato passa invariato e viene segnalato in interfaccia.
MAPPA_PATH = CONFIG_DIR / "varianti.csv"

_HEADER = ["taglia_bolla", "variante_gestionale", "note"]


def _crea_mappa_esempio() -> None:
    if MAPPA_PATH.exists():
        return
    with MAPPA_PATH.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(_HEADER)
        w.writerow(["# compilare con la corrispondenza reale del gestionale", "", ""])
        for t in ("XS", "S", "M", "L", "XL", "XXL", "3XL"):
            w.writerow([t, t, ""])
        w.writerow(["NS", "UNICA", "taglia unica / no size"])


def carica_mappa() -> dict[str, str]:
    _crea_mappa_esempio()
    mappa: dict[str, str] = {}
    with MAPPA_PATH.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            k = (row.get("taglia_bolla") or "").strip().upper()
            v = (row.get("variante_gestionale") or "").strip()
            if not k or k.startswith("#") or not v:
                continue
            mappa[k] = v
    return mappa


def normalizza_variante(taglia: str, mappa: dict[str, str] | None = None) -> tuple[str, bool]:
    """Traduce la taglia stampata in variante gestionale.

    Ritorna (variante, confermata). `confermata=False` significa che il valore
    e' una supposizione: l'interfaccia lo evidenzia e l'operatore decide.
    """
    t = taglia.strip().upper()
    mappa = carica_mappa() if mappa is None else mappa

    if t in mappa:
        return mappa[t], True

    if m := _MEZZA_TAGLIA.match(t):
        return f"{m.group('n')}.5", False

    if m := _ANNI_COMPATTO.match(t):
        a, b = int(m.group("a")), int(m.group("b"))
        if b == a + 1:  # 910A -> 9-10A, 1112 -> 11-12A
            return f"{a}-{b}A", False

    return t, False
