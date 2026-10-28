"""Ingest: da PDF/immagine a pagine normalizzate.

Produce due file per pagina:
  * `pNN.png`  ad alta risoluzione, per l'operatore che legge a schermo
  * `pNN.jpg`  ridotto a 1600px di lato lungo, e' quello inviato al modello
    (oltre quella soglia il costo cresce senza guadagno di accuratezza)
"""
from __future__ import annotations

import base64
import io
from dataclasses import dataclass
from pathlib import Path

import pymupdf
from PIL import Image

from .config import API_IMAGE_MAX_EDGE, PAGES_DIR, RENDER_DPI

IMMAGINI = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
FORMATI = IMMAGINI | {".pdf"}


class TroppePagine(ValueError):
    pass


@dataclass
class Pagina:
    numero: int
    png: Path
    jpg: Path
    rotazione_suggerita: int


def _profilo_inchiostro(img: Image.Image) -> tuple[float, float]:
    """Quanto 'somiglia a righe di testo' il profilo sui due assi.

    Righe di testo alternano molte bande piene e vuote lungo l'asse
    perpendicolare alle righe stesse; i righelli delle tabelle invece sono
    poche linee continue, e vanno scartati o falsano la misura.
    Precisione misurata sulle 14 pagine di esempio: 12/14. Resta un
    suggerimento: l'autorita' e' il campo `rotazione_gradi` che il modello
    riporta, piu' il pulsante di rotazione in interfaccia.
    """
    g = img.convert("L")
    g.thumbnail((900, 900))
    px = g.load()
    w, h = g.size
    righe = [0] * h
    colonne = [0] * w
    for y in range(h):
        for x in range(w):
            if px[x, y] < 190:  # inchiostro su fondo chiaro
                righe[y] += 1
                colonne[x] += 1

    def transizioni(profilo: list[int], lunghezza: int) -> float:
        # una riga/colonna quasi piena e' un righello di tabella, non testo
        pulito = [0 if v > 0.55 * lunghezza else v for v in profilo]
        if not any(pulito):
            return 0.0
        soglia = 0.25 * max(pulito)
        sopra = [v > soglia for v in pulito]
        cambi = sum(1 for i in range(len(sopra) - 1) if sopra[i] != sopra[i + 1])
        return cambi / len(sopra)

    return transizioni(righe, w), transizioni(colonne, h)


def rotazione_suggerita(img: Image.Image) -> int:
    """0 se la pagina sembra in piedi, 270 se sembra coricata.

    L'euristica sa dire *se* la pagina e' coricata, non da che parte: 270 e'
    il verso di entrambe le scansioni coricate degli esempi. Il verso esatto
    lo corregge il modello (`rotazione_gradi`) o l'operatore col pulsante.
    """
    orizz, vert = _profilo_inchiostro(img)
    return 270 if vert > orizz * 1.15 else 0


def _salva_pagina(img: Image.Image, dest_dir: Path, numero: int) -> Pagina:
    dest_dir.mkdir(parents=True, exist_ok=True)
    png = dest_dir / f"p{numero:03d}.png"
    jpg = dest_dir / f"p{numero:03d}.jpg"

    img.save(png)

    piccola = img.convert("RGB").copy()
    piccola.thumbnail((API_IMAGE_MAX_EDGE, API_IMAGE_MAX_EDGE), Image.LANCZOS)
    piccola.save(jpg, "JPEG", quality=85, optimize=True)

    return Pagina(numero, png, jpg, rotazione_suggerita(img))


def carica(percorso: Path, doc_id: str, max_pagine: int = 0) -> list[Pagina]:
    """Esplode un PDF o un'immagine nelle sue pagine normalizzate."""
    dest = PAGES_DIR / doc_id
    percorso = Path(percorso)

    if percorso.suffix.lower() in IMMAGINI:
        with Image.open(percorso) as img:
            return [_salva_pagina(img, dest, 1)]

    pagine: list[Pagina] = []
    with pymupdf.open(percorso) as doc:
        if max_pagine and doc.page_count > max_pagine:
            raise TroppePagine(
                f"il PDF ha {doc.page_count} pagine, il massimo e' {max_pagine}: dividilo"
            )
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=RENDER_DPI)
            with Image.open(io.BytesIO(pix.tobytes("png"))) as img:
                pagine.append(_salva_pagina(img, dest, i))
    return pagine


def da_immagini(immagini: list[Image.Image], doc_id: str) -> list[Pagina]:
    """Pagine gia' pronte, una per immagine: quelle della scansione da fotocamera."""
    dest = PAGES_DIR / doc_id
    return [_salva_pagina(img, dest, i) for i, img in enumerate(immagini, start=1)]


def come_base64(jpg: Path) -> str:
    return base64.standard_b64encode(jpg.read_bytes()).decode("ascii")
