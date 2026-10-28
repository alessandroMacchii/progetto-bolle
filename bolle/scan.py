"""Scansione da fotocamera: dalla foto di una bolla a una pagina dritta e pulita.

Tre passi, tutti visione artificiale classica (niente modelli):
  * `trova_angoli`  cerca il quadrilatero del foglio; l'operatore poi lo
                    corregge a mano trascinando gli angoli
  * `raddrizza`     trasformazione prospettica: quadrilatero -> rettangolo
  * `migliora`      toglie ombre e dominante di colore, alza il contrasto

Gli angoli viaggiano normalizzati 0..1 (x, y) rispetto alla foto: non
dipendono dalla risoluzione ne' dalla scala a cui l'interfaccia la mostra.

Niente bianco e nero "da scanner": la soglia cancellerebbe evidenziatore,
matita e penna rossa, cioe' proprio i segni che il modello deve leggere.
"""
from __future__ import annotations

import io

import cv2
import numpy as np
from PIL import Image, ImageOps

# lato lungo massimo della pagina raddrizzata: oltre non serve ne' a schermo
# ne' al modello (che riceve comunque 1600px, vedi ingest)
LATO_MAX = 2600
# lato su cui si cercano i bordi: piu' grande fa vedere il testo come bordi
LATO_RILEVAMENTO = 500
# un quadrilatero sotto questa frazione della foto non e' il foglio
AREA_MIN = 0.15

Angoli = list[list[float]]
TUTTA_LA_FOTO: Angoli = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]


def leggi(dati: bytes) -> np.ndarray:
    """Byte di una foto -> immagine BGR, girata come dice l'EXIF del telefono."""
    with Image.open(io.BytesIO(dati)) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def in_pil(img: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def jpeg(img: np.ndarray, qualita: int = 85) -> bytes:
    ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, qualita])
    if not ok:
        raise ValueError("codifica JPEG fallita")
    return buf.tobytes()


def riduci(img: np.ndarray, lato: int) -> np.ndarray:
    h, w = img.shape[:2]
    scala = lato / max(h, w)
    if scala >= 1:
        return img
    return cv2.resize(img, None, fx=scala, fy=scala, interpolation=cv2.INTER_AREA)


# --- rilevamento ---------------------------------------------------------------

def ordina(punti: np.ndarray) -> np.ndarray:
    """Alto-sinistra, alto-destra, basso-destra, basso-sinistra.

    Il trucco della somma x+y sbaglia col foglio girato di 45 gradi: qui si
    ordina per angolo attorno al baricentro, poi si parte dal punto piu'
    vicino all'angolo in alto a sinistra della foto.
    """
    p = np.asarray(punti, dtype=np.float32).reshape(4, 2)
    centro = p.mean(axis=0)
    p = p[np.argsort(np.arctan2(p[:, 1] - centro[1], p[:, 0] - centro[0]))]
    inizio = int(np.argmin(p.sum(axis=1)))
    return np.roll(p, -inizio, axis=0)


def _quadrilateri(binaria: np.ndarray, area_foto: float) -> list[tuple[float, np.ndarray]]:
    contorni, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    trovati = []
    for c in sorted(contorni, key=cv2.contourArea, reverse=True)[:5]:
        if cv2.contourArea(c) < AREA_MIN * area_foto:
            break
        # l'involucro convesso chiude le rientranze (un dito, un angolo piegato)
        involucro = cv2.convexHull(c)
        perimetro = cv2.arcLength(involucro, True)
        for tolleranza in (0.02, 0.03, 0.045, 0.06):
            poli = cv2.approxPolyDP(involucro, tolleranza * perimetro, True)
            if len(poli) == 4 and cv2.isContourConvex(poli):
                area = cv2.contourArea(poli)
                # quasi tutta la foto: e' il bordo dell'inquadratura, non il foglio
                if area < 0.97 * area_foto:
                    trovati.append((area, poli.reshape(4, 2)))
                break
    return trovati


def trova_angoli(img: np.ndarray) -> Angoli | None:
    """Angoli normalizzati del foglio, o None se nella foto non c'e' un quadrilatero."""
    piccola = riduci(img, LATO_RILEVAMENTO)
    h, w = piccola.shape[:2]
    grigio = cv2.GaussianBlur(cv2.cvtColor(piccola, cv2.COLOR_BGR2GRAY), (5, 5), 0)

    # due strade, si tiene il quadrilatero piu' grande:
    #  * i contorni (Canny), con soglie prese dalla luminosita' della foto
    #  * le zone chiare (Otsu): il foglio e' quasi sempre piu' chiaro del tavolo,
    #    e regge quando il bordo e' sfumato e Canny lo spezza
    mediana = float(np.median(grigio))
    bordi = cv2.Canny(grigio, int(max(0, 0.66 * mediana)), int(min(255, 1.33 * mediana)))
    bordi = cv2.dilate(bordi, np.ones((3, 3), np.uint8), iterations=2)
    _, chiare = cv2.threshold(grigio, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    chiare = cv2.morphologyEx(chiare, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))

    # Un foglio che esce dall'inquadratura non ha un contorno chiuso e non si
    # trova: lo sistema l'operatore con le maniglie. Chiudere le forme sul bordo
    # della foto e' stato provato, e inventa quadrilateri con ogni linea forte
    # che attraversa l'immagine (spigolo del tavolo, riflesso)
    candidati = _quadrilateri(bordi, w * h) + _quadrilateri(chiare, w * h)
    if not candidati:
        return None
    _, migliore = max(candidati, key=lambda c: c[0])
    angoli = ordina(migliore) / np.array([w, h], dtype=np.float32)
    return np.clip(angoli, 0, 1).astype(float).round(4).tolist()


def qualita(img: np.ndarray, angoli: Angoli | None) -> list[str]:
    """Problemi della foto da dire subito, mentre si puo' ancora rifarla.

    Solo avvisi: decide l'operatore. Soglie tarate sulle foto di prova, larghe
    apposta per non disturbare a vuoto.
    """
    avvisi = []
    grigio = cv2.cvtColor(riduci(img, 1200), cv2.COLOR_BGR2GRAY)
    # varianza del Laplaciano: misura quanti bordi netti ci sono. Il testo di
    # una bolla a fuoco ne ha tantissimi
    if cv2.Laplacian(grigio, cv2.CV_64F).var() < 40:
        avvisi.append("foto mossa o sfocata: rifalla tenendo fermo il telefono")
    if grigio.mean() < 70:
        avvisi.append("foto buia: accendi una luce o avvicinati alla finestra")
    # riflesso: macchia bruciata (bianco pieno) su una carta che per il resto
    # e' grigia. Una scansione vera e' tutta bianca piena, e non e' un riflesso
    if (grigio >= 252).mean() > 0.04 and np.percentile(grigio, 60) < 225:
        avvisi.append("c'e' un riflesso: inclina un po' il telefono o spegni il flash")
    if angoli is not None:
        area = cv2.contourArea(np.array(angoli, dtype=np.float32))
        if area < 0.3:
            avvisi.append("il foglio e' piccolo nella foto: avvicinati")
    return avvisi


# --- raddrizzamento --------------------------------------------------------------

def raddrizza(img: np.ndarray, angoli: Angoli) -> np.ndarray:
    """Porta il quadrilatero indicato su un rettangolo dritto."""
    h, w = img.shape[:2]
    p = ordina(np.array(angoli, dtype=np.float32) * np.array([w, h], dtype=np.float32))
    tl, tr, br, bl = p
    larghezza = max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl))
    altezza = max(np.linalg.norm(bl - tl), np.linalg.norm(br - tr))
    if min(larghezza, altezza) < 50:
        raise ValueError("angoli troppo vicini: allarga la selezione")
    scala = min(1.0, LATO_MAX / max(larghezza, altezza))
    W, H = int(larghezza * scala), int(altezza * scala)
    destinazione = np.array([[0, 0], [W - 1, 0], [W - 1, H - 1], [0, H - 1]], dtype=np.float32)
    matrice = cv2.getPerspectiveTransform(p, destinazione)
    return cv2.warpPerspective(img, matrice, (W, H), flags=cv2.INTER_CUBIC,
                               borderMode=cv2.BORDER_REPLICATE)


# --- miglioramento -------------------------------------------------------------

def togli_ombre(img: np.ndarray) -> np.ndarray:
    """Divide ogni canale per la carta stimata: ombre e luce gialla spariscono.

    La chiusura morfologica cancella i tratti sottili e scuri (le scritte) e
    lascia la carta con le sue sfumature di luce. Canale per canale, cosi' la
    carta torna bianca neutra mentre evidenziatore e penna, che sono diversi
    dalla carta, restano colorati. Lo sfondo si stima a meta' risoluzione: la
    luce varia piano, e costa un quarto.
    """
    h, w = img.shape[:2]
    piccola = cv2.resize(img, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    lato = max(15, (max(h, w) // 2) // 50) | 1  # piu' largo dei tratti, dispari
    nucleo = cv2.getStructuringElement(cv2.MORPH_RECT, (lato, lato))
    canali = []
    for canale, canale_piccolo in zip(cv2.split(img), cv2.split(piccola)):
        sfondo = cv2.morphologyEx(canale_piccolo, cv2.MORPH_CLOSE, nucleo)
        sfondo = cv2.medianBlur(sfondo, 21)
        sfondo = cv2.resize(sfondo, (w, h), interpolation=cv2.INTER_LINEAR)
        canali.append(cv2.divide(canale, np.maximum(sfondo, 1), scale=255))
    return cv2.merge(canali)


def livelli(img: np.ndarray, basso: float = 1, alto: float = 97, gamma: float = 1.25) -> np.ndarray:
    """Neri piu' neri e bianchi piu' bianchi; gamma > 1 rinforza i tratti chiari."""
    lo, hi = np.percentile(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (basso, alto))
    if hi - lo < 10:
        return img
    x = np.clip((img.astype(np.float32) - lo) / (hi - lo), 0, 1)
    return (x ** gamma * 255).astype(np.uint8)


def nitidezza(img: np.ndarray, forza: float = 0.5) -> np.ndarray:
    sfocata = cv2.GaussianBlur(img, (0, 0), 2)
    return cv2.addWeighted(img, 1 + forza, sfocata, -forza, 0)


def migliora(img: np.ndarray) -> np.ndarray:
    """Da foto a "scansione" a colori."""
    if cv2.cvtColor(riduci(img, 800), cv2.COLOR_BGR2GRAY).mean() < 90:
        # foto buia = rumorosa: schiarendola la grana si vedrebbe tutta
        img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
    return nitidezza(livelli(togli_ombre(img)))


def elabora(img: np.ndarray, angoli: Angoli, pulisci: bool) -> np.ndarray:
    pagina = raddrizza(img, angoli)
    return migliora(pagina) if pulisci else pagina
