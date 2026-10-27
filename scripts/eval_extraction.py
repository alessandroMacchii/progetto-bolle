"""Misura l'accuratezza dell'estrazione contro il gold set.

Script da riga di comando, nessun modulo lo importa:

    python scripts/eval_extraction.py "Esempio bolle.pdf"
    python scripts/eval_extraction.py "Esempio bolle.pdf" --backend mock
    python scripts/eval_extraction.py "Esempio bolle.pdf" --pagine 1,3,7
    python scripts/eval_extraction.py "Esempio bolle.pdf" --solo-coerenza

Serve a sapere se il prototipo funziona davvero, e a non peggiorarlo la
prossima volta che si tocca il prompt.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE))

from bolle.extract import crea_estrattore  # noqa: E402
from bolle.ingest import carica  # noqa: E402
from bolle.schema import PaginaEstratta  # noqa: E402
from bolle.sizes import colli, espandi, parse_size_qty  # noqa: E402

GOLD = RADICE / "gold" / "gold.json"


def normalizza_size(raw: str) -> str:
    """Confronto insensibile a spaziatura e maiuscole."""
    taglie, _ = parse_size_qty(raw)
    return " ".join(f"{t.taglia}/{t.qta}" for t in taglie)


def confronta_pagina(atteso: PaginaEstratta, ottenuto: PaginaEstratta) -> dict:
    """Righe appaiate per posizione: l'ordine di stampa e' quello del documento."""
    esiti: dict[str, list[bool]] = {
        "numero_documento": [atteso.numero_documento == ottenuto.numero_documento],
        "total_pieces": [atteso.total_pieces_dichiarato == ottenuto.total_pieces_dichiarato],
        "rotazione": [atteso.rotazione_gradi == ottenuto.rotazione_gradi],
        "n_righe": [len(atteso.righe) == len(ottenuto.righe)],
        "codice_articolo": [],
        "size_qty": [],
        "totale_riga": [],
        "barrata": [],
    }
    errori: list[str] = []

    for i, riga_attesa in enumerate(atteso.righe):
        if i >= len(ottenuto.righe):
            for campo in ("codice_articolo", "size_qty", "totale_riga", "barrata"):
                esiti[campo].append(False)
            errori.append(f"  riga {i + 1} mancante (attesa {riga_attesa.codice_articolo})")
            continue
        riga = ottenuto.righe[i]

        ok_codice = riga_attesa.codice_articolo.upper() == riga.codice_articolo.upper()
        ok_size = normalizza_size(riga_attesa.size_qty_raw) == normalizza_size(riga.size_qty_raw)
        ok_tot = riga_attesa.totale_dichiarato == riga.totale_dichiarato
        ok_barr = riga_attesa.barrata == riga.barrata

        esiti["codice_articolo"].append(ok_codice)
        esiti["size_qty"].append(ok_size)
        esiti["totale_riga"].append(ok_tot)
        esiti["barrata"].append(ok_barr)

        if not ok_codice:
            errori.append(
                f"  riga {i+1} codice: atteso {riga_attesa.codice_articolo!r}, "
                f"letto {riga.codice_articolo!r}"
            )
        if not ok_size:
            errori.append(
                f"  riga {i+1} taglie: atteso {riga_attesa.size_qty_raw!r}, "
                f"letto {riga.size_qty_raw!r}"
            )
        if not ok_tot:
            errori.append(
                f"  riga {i+1} Total: atteso {riga_attesa.totale_dichiarato}, "
                f"letto {riga.totale_dichiarato}"
            )
        if not ok_barr:
            errori.append(
                f"  riga {i+1} barrata: atteso {riga_attesa.barrata}, letto {riga.barrata}"
            )

    if len(ottenuto.righe) > len(atteso.righe):
        errori.append(f"  {len(ottenuto.righe) - len(atteso.righe)} righe di troppo")

    return {"esiti": esiti, "errori": errori}


def coerenza_gold(gold: dict) -> list[str]:
    """Il gold set deve quadrare da solo: sum(qta) == Total di riga."""
    problemi = []
    for numero, dati in gold.items():
        pagina = PaginaEstratta.model_validate(dati)
        for i, riga in enumerate(pagina.righe, 1):
            taglie, guasti = parse_size_qty(riga.size_qty_raw)
            if guasti:
                problemi.append(f"p{numero} riga {i}: {guasti}")
            somma = colli(taglie)
            if riga.totale_dichiarato and somma != riga.totale_dichiarato:
                problemi.append(
                    f"p{numero} riga {i}: somma {somma} != Total {riga.totale_dichiarato}"
                )
            if taglie != [x for t in riga.taglie for x in espandi(t.taglia, t.qta)]:
                problemi.append(f"p{numero} riga {i}: taglie scomposte non coerenti col grezzo")
    return problemi


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", help="PDF di esempio con le pagine del gold set")
    ap.add_argument("--backend", default=None, help="claude | mock | local")
    ap.add_argument("--pagine", default="", help="es. 1,3,7 (default: tutte)")
    ap.add_argument("--solo-coerenza", action="store_true", help="verifica solo il gold set")
    args = ap.parse_args()

    gold = json.loads(GOLD.read_text(encoding="utf-8"))

    print("=" * 72)
    print("COERENZA INTERNA DEL GOLD SET")
    print("=" * 72)
    problemi = coerenza_gold(gold)
    if problemi:
        print(f"{len(problemi)} incoerenze (attese dove la bolla stessa non quadra):")
        for p in problemi:
            print("  " + p)
    else:
        print("tutte le righe quadrano: sum(qta) == Total")
    if args.solo_coerenza:
        return 0

    filtro = {int(x) for x in args.pagine.split(",") if x.strip()} if args.pagine else None
    pagine = carica(Path(args.pdf), "_eval")
    try:
        estrattore = crea_estrattore(args.backend)
    except Exception as exc:  # tipicamente: credenziali mancanti
        print(f"\nImpossibile avviare l'estrattore: {exc}")
        return 1

    totali: dict[str, list[bool]] = {}
    print()
    print("=" * 72)
    print(f"ESTRAZIONE (backend: {args.backend or 'da configurazione'})")
    print("=" * 72)

    for pagina in pagine:
        if filtro and pagina.numero not in filtro:
            continue
        if str(pagina.numero) not in gold:
            continue
        atteso = PaginaEstratta.model_validate(gold[str(pagina.numero)])
        try:
            ottenuto = estrattore.estrai(pagina.jpg, pagina.numero)
        except Exception as exc:
            print(f"p{pagina.numero:02d}  ESTRAZIONE FALLITA: {type(exc).__name__}: {exc}")
            continue

        esito = confronta_pagina(atteso, ottenuto)
        for campo, valori in esito["esiti"].items():
            totali.setdefault(campo, []).extend(valori)

        tutti = [v for valori in esito["esiti"].values() for v in valori]
        segno = "OK " if all(tutti) else "ERR"
        print(f"{segno} p{pagina.numero:02d}  {sum(tutti)}/{len(tutti)} controlli superati")
        for e in esito["errori"]:
            print(e)

    print()
    print("=" * 72)
    print("RIEPILOGO PER CAMPO")
    print("=" * 72)
    for campo, valori in totali.items():
        if not valori:
            continue
        quota = sum(valori) / len(valori)
        barra = "#" * round(quota * 24)
        print(f"  {campo:18} {sum(valori):3}/{len(valori):<3} {quota:6.1%} {barra}")

    complessivo = [v for valori in totali.values() for v in valori]
    if complessivo:
        print(
            f"\n  TOTALE             {sum(complessivo)}/{len(complessivo)} "
            f"{sum(complessivo)/len(complessivo):.1%}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
