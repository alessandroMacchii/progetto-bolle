"""Configurazione centrale del prototipo."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = Path(os.getenv("BOLLE_DATA_DIR", ROOT / "data"))
PAGES_DIR = DATA_DIR / "pages"
UPLOAD_DIR = DATA_DIR / "uploads"
EXPORT_DIR = DATA_DIR / "export"
DB_PATH = DATA_DIR / "bolle.sqlite3"
CONFIG_DIR = ROOT / "config"

for _d in (DATA_DIR, PAGES_DIR, UPLOAD_DIR, EXPORT_DIR, CONFIG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# --- estrazione -------------------------------------------------------------
EXTRACTOR_BACKEND = os.getenv("BOLLE_EXTRACTOR", "claude")  # claude | openrouter | local | mock
MODEL = os.getenv("BOLLE_MODEL", "claude-opus-5")
# usato solo con BOLLE_EXTRACTOR=openrouter; id su https://openrouter.ai/models
OPENROUTER_MODEL = os.getenv("BOLLE_OPENROUTER_MODEL", "google/gemini-3.5-flash")

# Risoluzione di rendering. La PNG ad alta risoluzione serve all'operatore per
# leggere la bolla a schermo; la JPEG ridotta e' quella che viaggia verso il
# modello (oltre ~1600px il lato lungo non aggiunge accuratezza, solo costo).
RENDER_DPI = int(os.getenv("BOLLE_RENDER_DPI", "200"))
API_IMAGE_MAX_EDGE = int(os.getenv("BOLLE_API_MAX_EDGE", "1600"))

# --- magazzini --------------------------------------------------------------
MAGAZZINI = [m.strip() for m in os.getenv("BOLLE_MAGAZZINI", "MAG 1,MAG 2").split(",")]
MAGAZZINO_DEFAULT = MAGAZZINI[0]

# --- export -----------------------------------------------------------------
# Intestazioni del file destinato all'import nel gestionale.
# DA CONFERMARE con l'azienda (vedi README, "Domande aperte").
EXCEL_HEADERS = [
    h.strip()
    for h in os.getenv(
        "BOLLE_EXCEL_HEADERS", "Magazzino,Codice Articolo,Variante,Quantita"
    ).split(",")
]
