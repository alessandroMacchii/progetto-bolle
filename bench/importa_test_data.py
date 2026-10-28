"""Costruisce il banco di prova dal ground truth di `test_data/`.

    python bench/importa_test_data.py

`test_data/X.json` (schema `test_data/schema_bolla.json`) accanto a `X.pdf`
descrive il CARICO: una riga per taglia, con le correzioni a mano gia'
applicate (la taglia e' `4-`, non lo `550` stampato). Non si puo' quindi
tradurre nell'`atteso` dei casi di `genera.py`, che descrive lo stampato: il
confronto si fa dopo `costruisci_righe` (vedi `punteggio.valuta_carico`).

Produce `bench/casi/td-*.jpg` e `bench/casi/casi_test_data.json`, che
`esegui.py` e `report.py` leggono (insieme a `casi.json`, se `genera.py` lo
ricrea). Il campo `note_estrazione` del ground truth e' ignorato: sono appunti
di chi l'ha compilato. Le righe barrate sulla bolla nel ground truth non ci
sono: non entrano nel carico.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

import pymupdf
from PIL import Image

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE))

from bolle.config import API_IMAGE_MAX_EDGE, RENDER_DPI  # noqa: E402

BENCH = RADICE / "bench"
CASI = BENCH / "casi"
TEST_DATA = RADICE / "test_data"
USCITA = CASI / "casi_test_data.json"


def _id_caso(nome: str) -> str:
    return "td-" + nome.lower().replace(" ", "-")


def _salva_jpg(pdf: Path, dest: Path) -> None:
    """Stessa resa di `bolle/ingest.py`: si misura l'immagine che vede l'app."""
    with pymupdf.open(pdf) as doc:
        if doc.page_count != 1:
            raise ValueError(f"{doc.page_count} pagine: il banco lavora a pagina singola")
        pix = doc[0].get_pixmap(dpi=RENDER_DPI)
    with Image.open(io.BytesIO(pix.tobytes("png"))) as img:
        piccola = img.convert("RGB")
        piccola.thumbnail((API_IMAGE_MAX_EDGE, API_IMAGE_MAX_EDGE), Image.LANCZOS)
        piccola.save(dest, "JPEG", quality=85, optimize=True)


def _atteso_carico(gt: dict) -> list[dict]:
    return [
        {
            "seq": str(r["numero_progressivo"]),
            "codice_articolo": r["numero_articolo"].strip().upper(),
            "taglia": r["taglia"].strip().upper(),
            "qta": r["quantita_taglia"],
            "magazzino": r["magazzino"] or "",
            "barrata": r["riga_barrata"],
        }
        for r in gt["righe"]
    ]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    casi = []
    for f in sorted(TEST_DATA.glob("*.json")):
        if f.name == "schema_bolla.json":
            continue
        pdf = f.with_suffix(".pdf")
        gt = json.loads(f.read_text(encoding="utf-8"))
        if not pdf.exists():
            print(f"salto {f.name}: manca {pdf.name}")
            continue
        if not gt["righe"]:
            print(f"salto {f.name}: ground truth senza righe")
            continue
        if any(r["riga_barrata"] for r in gt["righe"]):
            # per convenzione le righe cancellate non si mettono nel ground truth
            print(f"attenzione {f.name}: contiene righe barrate, che il carico non avra'")

        id_caso = _id_caso(f.stem)
        try:
            _salva_jpg(pdf, CASI / f"{id_caso}.jpg")
        except ValueError as exc:
            print(f"salto {f.name}: {exc}")
            continue
        casi.append({
            "id": id_caso,
            "famiglia": "test_data",
            "base": f"test_data/{pdf.name}",
            "descrizione": f"ground truth di test_data ({f.stem})",
            "etichette": ["carico"],
            "immagine": f"{id_caso}.jpg",
            "numero_documento": gt["delivery_note"],
            "atteso_carico": _atteso_carico(gt),
        })
        print(f"ok    {f.name} -> {id_caso} ({len(gt['righe'])} righe di carico)")

    USCITA.write_text(json.dumps(casi, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(casi)} casi in {USCITA.relative_to(RADICE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
