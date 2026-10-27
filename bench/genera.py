"""Costruisce il banco di prova: `bench/casi/*.jpg` + `bench/casi/casi.json`.

    python bench/genera.py

Tre famiglie di casi:

  reale-NN   le 14 pagine di `Esempio bolle.pdf`, con la calligrafia VERA
             (atteso: gold/gold.json)
  pulita-*   le 4 pagine di `altrebolle/`, cosi' come sono arrivate
  sint-*     le stesse 4 pagine con annotazioni disegnate sopra: magazzini,
             evidenziatore, cerchi, righe barrate, correzioni, graffe, matita,
             piu' i difetti di scansione (rotazione, foto storta, fax)

Le annotazioni sintetiche usano font "a mano" di Windows: sono piu' regolari di
una calligrafia vera, quindi un modello che sbaglia qui sbagliera' anche sul
vero, ma non vale il contrario. Il riferimento per la calligrafia restano i
casi `reale-*`.
"""
from __future__ import annotations

import io
import json
import math
import random
import re
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pagine_nuove import PAGINE, pagina_attesa  # noqa: E402

CASI = RADICE / "bench" / "casi"
FONT_DIR = Path("C:/Windows/Fonts")
LATO_LUNGO = 1600  # come bolle/ingest.py: e' quello che vede il modello

FONT = {
    "script": "segoesc.ttf",
    "ink": "Inkfree.ttf",
    "print": "segoepr.ttf",
    "boli": "mvboli.ttf",
}
INCHIOSTRO = {
    "blu": ((28, 48, 150), 235),
    "nera": ((25, 25, 30), 240),
    "rossa": ((190, 30, 35), 230),
    "matita": ((105, 105, 112), 185),
}
EVIDENZIATORE = {"giallo": (255, 243, 80), "verde": (150, 240, 130), "azzurro": (130, 215, 250)}

_MAG = re.compile(r"\bMAG\s*(\d+)\b", re.IGNORECASE)


def rendi_pdf(percorso: Path, indice: int = 0, dpi: int = 200) -> Image.Image:
    with pymupdf.open(percorso) as doc:
        pix = doc[indice].get_pixmap(dpi=dpi)
        return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")


class Penna:
    """Disegna sulla pagina come farebbe un magazziniere, con un po' di tremolio."""

    def __init__(self, img: Image.Image, seme: int, font: str = "ink", inchiostro: str = "blu"):
        self.img = img
        self.rng = random.Random(seme)
        self.font = font
        self.inchiostro = inchiostro

    def _colore(self, inchiostro: str | None):
        rgb, alpha = INCHIOSTRO[inchiostro or self.inchiostro]
        return rgb + (alpha,)

    def testo(self, txt, cx, cy, size=40, inchiostro=None, font=None, angolo=None):
        f = ImageFont.truetype(str(FONT_DIR / FONT[font or self.font]), size)
        l, t, r, b = f.getbbox(txt)
        strato = Image.new("RGBA", (r - l + 20, b - t + 20), (0, 0, 0, 0))
        ImageDraw.Draw(strato).text((10 - l, 10 - t), txt, font=f, fill=self._colore(inchiostro))
        if angolo is None:
            angolo = self.rng.uniform(-6, 6)
        strato = strato.rotate(angolo, expand=True, resample=Image.BICUBIC)
        x = int(cx - strato.width / 2 + self.rng.uniform(-4, 4))
        y = int(cy - strato.height / 2 + self.rng.uniform(-3, 3))
        self.img.paste(strato, (x, y), strato)
        return (x, y, x + strato.width, y + strato.height)

    def _tratto(self, punti, inchiostro=None, spessore=4):
        strato = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(strato).line(punti, fill=self._colore(inchiostro), width=spessore, joint="curve")
        self.img.paste(strato, (0, 0), strato)

    def linea(self, x0, y0, x1, y1, inchiostro=None, spessore=4, tremolio=4):
        n = 8
        punti = [
            (
                x0 + (x1 - x0) * i / n + self.rng.uniform(-tremolio, tremolio),
                y0 + (y1 - y0) * i / n + self.rng.uniform(-tremolio, tremolio),
            )
            for i in range(n + 1)
        ]
        self._tratto(punti, inchiostro, spessore)

    def cerchio(self, box, inchiostro=None, spessore=4):
        x0, y0, x1, y1 = box
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 12, (y1 - y0) / 2 + 8
        inizio = self.rng.uniform(0, 6.28)
        punti = []
        for i in range(34):  # un giro e un pezzetto: i cerchi a mano non chiudono
            a = inizio + i * 6.9 / 33
            k = 1 + self.rng.uniform(-0.05, 0.05)
            punti.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
        self._tratto(punti, inchiostro, spessore)

    def evidenzia(self, box, colore="giallo"):
        x0, y0, x1, y1 = [int(v) for v in box]
        x0, y0, x1, y1 = x0 - 10, y0 - 4, x1 + 10, y1 + 4
        zona = self.img.crop((x0, y0, x1, y1))
        tinta = Image.new("RGB", zona.size, EVIDENZIATORE[colore])
        self.img.paste(ImageChops.multiply(zona, tinta), (x0, y0))

    def ics(self, cx, cy, r=22, inchiostro=None):
        self.linea(cx - r, cy - r, cx + r, cy + r, inchiostro, tremolio=2)
        self.linea(cx - r, cy + r, cx + r, cy - r, inchiostro, tremolio=2)

    def spunta(self, cx, cy, inchiostro=None):
        self._tratto([(cx - 14, cy), (cx - 4, cy + 13), (cx + 20, cy - 18)], inchiostro, 4)

    def graffa(self, x, y0, y1, inchiostro=None):
        self._tratto(
            [(x - 14, y0 - 12), (x, y0), (x + 3, (y0 + y1) / 2), (x, y1), (x - 14, y1 + 12)],
            inchiostro,
            4,
        )


# --- ricette -----------------------------------------------------------------
# Ogni ricetta disegna sulla pagina e ritorna {seq: {...}} con cio' che
# l'estrazione DEVE riportare per quella riga, oltre ai dati stampati:
#   mag      magazzini scritti a mano che si riferiscono alla riga
#   barrata  la riga e' cancellata
#   parole   parole che la trascrizione delle annotazioni deve contenere

def _riga(p, seq):
    return next(r for r in p["righe"] if r[0] == seq)


def _cx(intervallo):
    return (intervallo[0] + intervallo[1]) / 2


def mag_per_riga(penna, p, assegnazioni, zona="prezzo", size=40, stile=None, colore_evid=None):
    """`MAG n` accanto a ogni riga. stile: None | 'evidenziato' | 'cerchiato'."""
    atteso = {}
    ultima_y = -999
    for seq, mag in assegnazioni.items():
        y = _riga(p, seq)[6] + 4
        # righe a 37 px l'una dall'altra: nessuno ci scrive due sigle sovrapposte,
        # la seconda resta senza annotazione (e l'atteso lo sa)
        if y - ultima_y < 60:
            continue
        ultima_y = y
        if zona == "prezzo":
            cx = _cx(p["x"]["prezzo"])
        elif zona == "nome":
            cx = p["x"]["nome"] + 560
        else:  # sopra le taglie: il caso cattivo, la penna copre lo stampato
            cx = _cx(p["x"]["taglie"]) + 20
        box = penna.testo(mag, cx, y, size=size)
        if stile == "evidenziato":
            penna.evidenzia(box, colore_evid or "giallo")
        elif stile == "cerchiato":
            penna.cerchio(box)
        atteso[seq] = {"mag": [mag]}
    return atteso


def barra_riga(penna, p, seq, inchiostro=None):
    y = _riga(p, seq)[6] + 6
    penna.linea(p["x"]["sx"] + 30, y + penna.rng.uniform(-6, 6), p["x"]["dx"] - 20,
                y + penna.rng.uniform(-10, 10), inchiostro, spessore=5, tremolio=5)
    return {seq: {"barrata": True}}


def ics_su_seq(penna, p, seq, inchiostro=None):
    # sulla consolidata il numero di riga sta a ridosso della colonna Article
    x = p["x"]["sx"] + (88 if p["tipo_documento"].startswith("CONSOLIDATED") else 60)
    penna.ics(x, _riga(p, seq)[6] + 4, inchiostro=inchiostro)
    return {seq: {"barrata": True}}


def unisci(*parti):
    fuori: dict = {}
    for parte in parti:
        for seq, v in parte.items():
            voce = fuori.setdefault(seq, {})
            for k, val in v.items():
                if k in ("mag", "parole"):
                    voce[k] = voce.get(k, []) + [x for x in val if x not in voce.get(k, [])]
                else:
                    voce[k] = val
    return fuori


def alterna(p, schema):
    return {r[0]: schema[i % len(schema)] for i, r in enumerate(p["righe"])}


# --- difetti di scansione ----------------------------------------------------

def ruota(img, gradi_orari):
    return img.rotate(-gradi_orari, expand=True)


def foto_telefono(img, seme):
    rng = random.Random(seme)
    img = img.rotate(rng.choice([-4, 3.5]), expand=True, fillcolor=(232, 228, 220), resample=Image.BICUBIC)
    w, h = img.size
    ombra = Image.linear_gradient("L").rotate(35, expand=True).resize((w, h))
    ombra = ImageEnhance.Brightness(ombra).enhance(0.55).point(lambda v: 150 + v * 105 // 255)
    img = ImageChops.multiply(img, Image.merge("RGB", (ombra, ombra, ombra)))
    return img.filter(ImageFilter.GaussianBlur(1.3))


def fax(img):
    grigio = img.convert("L").resize((img.width // 2, img.height // 2), Image.BILINEAR)
    return grigio.point(lambda v: 255 if v > 165 else 0).convert("RGB")


def salva(img, nome, lato=LATO_LUNGO, qualita=85):
    img = img.convert("RGB")
    img.thumbnail((lato, lato), Image.LANCZOS)
    img.save(CASI / nome, "JPEG", quality=qualita, optimize=True)


# --- costruzione dei casi ----------------------------------------------------

def caso_sintetico(nome, base, descrizione, etichette, ricetta, seme, font="ink", inchiostro="blu",
                   dopo=None, rotazione=0, lato=LATO_LUNGO, qualita=85):
    p = PAGINE[base]
    img = rendi_pdf(RADICE / "altrebolle" / p["file"])
    penna = Penna(img, seme, font, inchiostro)
    modifiche = ricetta(penna, p) if ricetta else {}
    if dopo:
        img = dopo(img)
    if rotazione:
        img = ruota(img, rotazione)
    salva(img, f"{nome}.jpg", lato, qualita)

    atteso = pagina_attesa(base)
    atteso["rotazione_gradi"] = (360 - rotazione) % 360
    extra = []
    for riga in atteso["righe"]:
        m = modifiche.get(riga["seq"], {})
        riga["barrata"] = bool(m.get("barrata"))
        riga["correzioni"] = m.get("correzioni", [])
        riga["annotazioni_manoscritte"] = "; ".join(
            m.get("mag", []) + (["riga barrata"] if m.get("barrata") else []) + m.get("parole", [])
        )
        extra.append({"mag": sorted(m.get("mag", [])), "parole": m.get("parole", [])})
    return {
        "id": nome,
        "famiglia": "sintetica" if ricetta or dopo or rotazione else "pulita",
        "base": base,
        "descrizione": descrizione,
        "etichette": etichette,
        "immagine": f"{nome}.jpg",
        "atteso": atteso,
        "righe_extra": extra,
    }


# codici coperti dalla penna al punto da non essere verificabili nemmeno a
# occhio: si accettano entrambe le letture plausibili
CODICI_AMMESSI = {("7", 3): ["JZ6878", "JZ6678"]}

# parole che la trascrizione delle annotazioni vere deve contenere
PAROLE_REALI = {
    ("8", 0): ["5"],
    ("9", 0): ["VERONELLI"],
    ("9", 2): ["BRENTASPORT"],
    ("14", 0): ["JN9131"],
}


def casi_reali():
    gold = json.loads((RADICE / "gold" / "gold.json").read_text(encoding="utf-8"))
    casi = []
    for numero, atteso in gold.items():
        nome = f"reale-{int(numero):02d}"
        salva(rendi_pdf(RADICE / "Esempio bolle.pdf", int(numero) - 1), f"{nome}.jpg")
        extra = []
        for i, riga in enumerate(atteso["righe"]):
            mag = sorted({f"MAG {n}" for n in _MAG.findall(riga["annotazioni_manoscritte"])})
            extra.append({"mag": mag, "parole": PAROLE_REALI.get((numero, i), []),
                          "codici": CODICI_AMMESSI.get((numero, i), [])})
        casi.append(
            {
                "id": nome,
                "famiglia": "reale",
                "base": f"esempio p{numero}",
                "descrizione": "pagina di esempio con calligrafia vera",
                "etichette": ["calligrafia vera"],
                "immagine": f"{nome}.jpg",
                "atteso": atteso,
                "righe_extra": extra,
            }
        )
    return casi


def tutti_i_casi():
    C, P1, P2, P3 = (PAGINE[k] for k in ("C", "P1", "P2", "P3"))
    M1, M2 = "MAG 1", "MAG 2"
    casi = casi_reali()
    aggiungi = lambda *a, **k: casi.append(caso_sintetico(*a, **k))  # noqa: E731

    for base in ("C", "P1", "P2", "P3"):
        aggiungi(f"pulita-{base}", base, "bolla bianca, come arrivata", ["pulita"], None, 0)

    # --- magazzini: i modi di scriverli ---
    aggiungi("sint-C-mag-penna", "C", "MAG a penna blu su ogni riga", ["mag"],
             lambda pn, p: mag_per_riga(pn, p, {"1": M1, "2": M2, "3": M1, "4": M2}, size=46), 11)
    aggiungi("sint-C-mag-evidenziato", "C", "MAG a penna nera evidenziato in giallo/verde, sopra le taglie", ["mag", "evidenziatore"],
             lambda pn, p: unisci(
                 mag_per_riga(pn, p, {"1": M1, "3": M1}, zona="nome", size=44, stile="evidenziato"),
                 mag_per_riga(pn, p, {"2": M2, "4": M2}, zona="nome", size=44, stile="evidenziato",
                              colore_evid="verde")), 12, font="print", inchiostro="nera")
    aggiungi("sint-C-mag-cerchiato-matita", "C", "MAG a MATITA, cerchiato", ["mag", "matita", "cerchio"],
             lambda pn, p: mag_per_riga(pn, p, {"1": M2, "2": M2, "3": M1, "4": M1}, size=46,
                                        stile="cerchiato"), 13, font="script", inchiostro="matita")

    def split(pn, p):
        y = _riga(p, "1")[6]
        pn.testo("2 MAG 1", 1010, y + 75, size=36)
        pn.testo("1 MAG 2", 1010, y + 120, size=36)
        pn.linea(985, y + 22, 1000, y + 55, tremolio=2)  # freccia dalla taglia XS/3
        return unisci({"1": {"mag": [M1, M2]}}, mag_per_riga(pn, p, {"2": M1, "3": M2, "4": M2}, size=44))
    aggiungi("sint-C-split-taglia", "C", "una taglia divisa su due magazzini (2 MAG 1 + 1 MAG 2)",
             ["mag", "split"], split, 14)

    aggiungi("sint-C-barrate", "C", "riga 3 cancellata con un tratto, riga 4 con X sul numero",
             ["barrate", "mag"],
             lambda pn, p: unisci(mag_per_riga(pn, p, {"1": M1, "2": M1}, size=44),
                                  barra_riga(pn, p, "3"), ics_su_seq(pn, p, "4")), 15, inchiostro="nera")

    def correzione(pn, p):
        y = _riga(p, "1")[6]
        pn.linea(1118, y + 2, 1168, y - 2, spessore=4, tremolio=2)  # tratto su S/5
        pn.testo("4", 1190, y - 30, size=44, angolo=4)
        return unisci({"1": {"parole": ["4"], "correzioni": [
            {"taglia_stampata": "S", "taglia_corretta": "", "qta_corretta": 4}]}},
            mag_per_riga(pn, p, {"1": M1, "2": M2}, size=44))
    aggiungi("sint-C-qta-corretta", "C", "quantita' stampata S/5 barrata e corretta a mano in 4",
             ["correzione", "mag"], correzione, 16)

    # --- pagine dense ---
    aggiungi("sint-P1-mag-ogni-riga", "P1", "11 righe fitte, MAG su ognuna", ["mag", "denso"],
             lambda pn, p: mag_per_riga(pn, p, alterna(p, [M1, M1, M2]), size=40), 21, font="print")

    def graffe(pn, p):
        x = p["x"]["dx"] + 14
        pn.graffa(x, _riga(p, "1")[6] - 12, _riga(p, "2")[6] + 30)
        pn.testo("M2", x + 34, _riga(p, "1")[6] + 22, size=34, angolo=0)
        pn.graffa(x, _riga(p, "3")[6] - 12, _riga(p, "11")[6] + 30)
        pn.testo("M1", x + 34, _riga(p, "7")[6], size=34, angolo=0)
        return {r[0]: {"mag": [M2 if r[0] in ("1", "2") else M1]} for r in p["righe"]}
    aggiungi("sint-P1-graffe", "P1", "due graffe a margine: 'M2' per le righe 1-2, 'M1' per 3-11",
             ["mag", "graffa", "abbreviazione", "denso"], graffe, 22)

    def spunte(pn, p):
        for r in p["righe"]:
            pn.spunta(p["x"]["sx"] - 28, r[6] + 2)
        pn.testo("ok 8 colli", 1150, 2110, size=44)
        return {}
    aggiungi("sint-P1-solo-spunte", "P1", "solo spunte di controllo e 'ok 8 colli': nessun magazzino",
             ["rumore"], spunte, 23, inchiostro="rossa", font="boli")

    aggiungi("sint-P1-mix", "P1", "MAG su alcune righe, 2 barrate, 1 con X, spunte",
             ["mag", "barrate", "denso"],
             lambda pn, p: unisci(
                 mag_per_riga(pn, p, {"1": M1, "3": M2, "4": M2, "6": M1, "9": M2, "11": M1}, size=40),
                 barra_riga(pn, p, "5"), barra_riga(pn, p, "8"), ics_su_seq(pn, p, "10")), 24, font="print")

    aggiungi("sint-P2-evidenziati", "P2", "15 righe, MAG evidenziato su ognuna, 2 righe barrate",
             ["mag", "evidenziatore", "barrate", "denso"],
             lambda pn, p: unisci(
                 mag_per_riga(pn, p, alterna(p, [M1, M2]), size=38, stile="evidenziato"),
                 barra_riga(pn, p, "16"), barra_riga(pn, p, "24")), 31, font="print", inchiostro="nera")
    aggiungi("sint-P2-matita", "P2", "15 righe, MAG a MATITA leggera", ["mag", "matita", "denso"],
             lambda pn, p: mag_per_riga(pn, p, alterna(p, [M2, M1, M1]), size=42), 32,
             font="script", inchiostro="matita")

    def codice_a_mano(pn, p):
        fuori = mag_per_riga(pn, p, alterna(p, [M1, M2, M2]), size=38)
        pn.testo("VERONELLI", 760, _riga(p, "29")[6] + 60, size=40)
        pn.testo("JN9131 x 3", 760, _riga(p, "32")[6] + 70, size=40)
        return unisci(fuori, {"29": {"parole": ["VERONELLI"]}})
    aggiungi("sint-P3-rossa-codice", "P3", "17 righe, penna rossa, nome cliente e codice aggiunti a mano",
             ["mag", "codice a mano", "denso"], codice_a_mano, 41, inchiostro="rossa", font="boli")

    def mag_di_pagina(pn, p):
        box = pn.testo("TUTTO MAG 2", 820, 150, size=70, angolo=-3)
        pn.cerchio(box)
        return {r[0]: {"mag": [M2]} for r in p["righe"]}
    aggiungi("sint-P2-mag-di-pagina", "P2", "un solo 'TUTTO MAG 2' in testa alla pagina",
             ["mag", "mag di pagina"], mag_di_pagina, 42)

    aggiungi("sint-P3-sopra-taglie", "P3", "MAG scritto SOPRA la colonna Size/Qty: copre lo stampato",
             ["mag", "copre lo stampato", "denso"],
             lambda pn, p: mag_per_riga(pn, p, {"28": M1, "29": M2, "30": M1, "31": M2, "32": M2,
                                                "37": M1, "40": M2, "43": M1}, zona="taglie", size=40),
             43, inchiostro="nera", font="script")

    # --- difetti di scansione ---
    aggiungi("sint-P1-ruotata-90", "P1", "scansione coricata (90 gradi) con MAG", ["mag", "rotazione"],
             lambda pn, p: mag_per_riga(pn, p, alterna(p, [M2, M1]), size=40), 51, rotazione=90, font="print")
    aggiungi("sint-P2-capovolta", "P2", "scansione capovolta (180 gradi), pulita", ["rotazione"],
             None, 52, rotazione=180)
    aggiungi("sint-C-foto-telefono", "C", "foto da telefono: storta, in ombra, sfocata, compressa",
             ["mag", "foto"],
             lambda pn, p: mag_per_riga(pn, p, {"1": M1, "2": M2, "3": M2, "4": M1}, size=46), 53,
             dopo=lambda im: foto_telefono(im, 53), lato=1200, qualita=40)
    aggiungi("sint-P3-fax", "P3", "bianco e nero a bassa risoluzione (fax/fotocopia)", ["mag", "fax"],
             lambda pn, p: mag_per_riga(pn, p, alterna(p, [M1, M2]), size=40), 54, font="print",
             inchiostro="nera", dopo=fax)
    return casi


def main() -> None:
    CASI.mkdir(parents=True, exist_ok=True)
    casi = tutti_i_casi()
    (CASI / "casi.json").write_text(json.dumps(casi, ensure_ascii=False, indent=1), encoding="utf-8")
    per_famiglia: dict[str, int] = {}
    for c in casi:
        per_famiglia[c["famiglia"]] = per_famiglia.get(c["famiglia"], 0) + 1
    print(f"{len(casi)} casi in {CASI}: {per_famiglia}")
    print(f"righe totali: {sum(len(c['atteso']['righe']) for c in casi)}")


if __name__ == "__main__":
    main()
