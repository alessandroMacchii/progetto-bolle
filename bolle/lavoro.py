"""Dalla pagina estratta alle righe di lavoro editabili dall'operatore.

Una `RigaLavoro` e' una riga per singola taglia: e' l'unita' che l'operatore
vede a schermo ed e' l'unita' che finisce nell'Excel. Qui vengono applicati i
controlli deterministici (parsing Size/Qty, quadratura dei totali,
normalizzazione della variante) che non richiedono un modello.
"""
from __future__ import annotations

import re
import uuid

from .config import MAGAZZINI, MAGAZZINO_DEFAULT
from .schema import PaginaEstratta, RigaEstratta, RigaLavoro
from .sizes import (
    TagliaQta,
    carica_mappa,
    colli,
    espandi,
    normalizza_variante,
    parse_size_qty,
    verifica_totale,
)

# "MAG 1", "MAG1", "mag 2" nelle annotazioni trascritte dal modello.
_MAG = re.compile(r"\bMAG\s*(\d+)\b", re.IGNORECASE)
# "MAG ?": il modello ha visto una sigla di magazzino ma non la cifra.
_MAG_ILLEGGIBILE = re.compile(r"\bMAG\s*\?", re.IGNORECASE)


def _magazzini_citati(annotazione: str) -> list[str]:
    """Magazzini nominati nella calligrafia, nell'ordine in cui compaiono."""
    visti: list[str] = []
    for numero in _MAG.findall(annotazione or ""):
        etichetta = f"MAG {numero}"
        if etichetta in MAGAZZINI and etichetta not in visti:
            visti.append(etichetta)
    return visti


def _taglie_di_riga(riga: RigaEstratta) -> tuple[list[TagliaQta], list[str]]:
    """Taglie della riga, preferendo il parsing deterministico del grezzo.

    Il modello restituisce gia' `taglie` scomposte, ma la stringa `size_qty_raw`
    e' verificabile con una regex: quando le due letture divergono lo diciamo,
    invece di sceglierne una in silenzio.
    """
    avvisi: list[str] = []
    da_regex, problemi = parse_size_qty(riga.size_qty_raw)
    da_modello = [x for t in riga.taglie for x in espandi(t.taglia, t.qta)]

    if not da_regex:
        avvisi.extend(problemi)
        return da_modello, avvisi

    # un token scartato e' un collo che sparisce dal carico: va detto
    avvisi.extend(problemi)
    if da_modello and da_regex != da_modello:
        avvisi.append(
            "lettura discorde: colonna grezza "
            f"{[(t.taglia, t.qta) for t in da_regex]} vs scomposizione "
            f"{[(t.taglia, t.qta) for t in da_modello]}"
        )
    return da_regex, avvisi


def costruisci_righe(pagina: PaginaEstratta, numero_pagina: int) -> list[RigaLavoro]:
    mappa = carica_mappa()
    righe: list[RigaLavoro] = []

    for riga in pagina.righe:
        taglie, avvisi_riga = _taglie_di_riga(riga)

        avvisi_riga += verifica_totale(taglie, riga.totale_dichiarato)

        if not riga.codice_articolo:
            avvisi_riga.append("codice articolo non letto: da inserire a mano")
        if riga.barrata:
            avvisi_riga.append("riga barrata a penna sulla bolla: esclusa per default")
        if riga.incertezze:
            avvisi_riga.append(f"lettura incerta: {riga.incertezze}")
        if riga.codice_manoscritto:
            avvisi_riga.append(
                f"sulla bolla c'e' un codice scritto a mano ({riga.codice_manoscritto}) "
                f"diverso da quello stampato ({riga.codice_articolo or 'non letto'})"
            )

        citati = _magazzini_citati(riga.annotazioni_manoscritte)
        if not citati and not riga.barrata:
            # nessuna sigla sulla riga: vale quella scritta per tutta la pagina
            citati = _magazzini_citati(pagina.magazzino_pagina)
        if len(citati) == 1:
            magazzino = citati[0]
            # la sigla e' una sola e leggibile: si applica senza chiedere
            avvisi_riga.append(f"magazzino proposto dall'annotazione a mano ({magazzino})")
        else:
            magazzino = MAGAZZINO_DEFAULT
            if _MAG_ILLEGGIBILE.search(
                f"{riga.annotazioni_manoscritte} {pagina.magazzino_pagina}"
            ):
                avvisi_riga.append(
                    "magazzino scritto a mano ma illeggibile: indicare dove va"
                )
            elif len(citati) > 1:
                avvisi_riga.append(
                    "l'annotazione a mano cita piu' magazzini "
                    f"({', '.join(citati)}): assegnare riga per riga o usare Dividi"
                )

        for t in taglie:
            taglia, qta = t.taglia, t.qta
            variante, confermata = normalizza_variante(taglia, mappa)
            avvisi = list(avvisi_riga)
            if t.pacco:
                avvisi.append(
                    f"dal pacco misto '{t.pacco}': ogni pacco contiene una "
                    f"{' + una '.join(t.pacco.split('/'))}"
                )
            if not confermata:
                avvisi.append(
                    f"variante '{variante}' dedotta dalla taglia '{taglia}' "
                    "(non presente in config/varianti.csv)"
                )
            righe.append(
                RigaLavoro(
                    id=uuid.uuid4().hex[:12],
                    pagina=numero_pagina,
                    seq=riga.seq,
                    codice_articolo=riga.codice_articolo,
                    descrizione=riga.descrizione,
                    colore=riga.colore,
                    taglia=taglia,
                    variante=variante,
                    variante_confermata=confermata,
                    qta=qta,
                    pacco=t.pacco,
                    magazzino=magazzino,
                    eliminata=riga.barrata,
                    origine="estratta",
                    avvisi=avvisi,
                    annotazioni_manoscritte=riga.annotazioni_manoscritte,
                )
            )

    return righe


def verifica_pagina(pagina: PaginaEstratta, righe: list[RigaLavoro]) -> list[str]:
    """Controlli a livello di pagina: il secondo checksum, sul totale colli."""
    avvisi: list[str] = []
    if pagina.total_pieces_dichiarato > 0:
        somma = colli(
            [TagliaQta(r.taglia, r.qta, r.pacco) for r in righe if not r.eliminata]
        )
        if somma != pagina.total_pieces_dichiarato:
            avvisi.append(
                f"totale pagina {somma} != Total Pieces stampato "
                f"{pagina.total_pieces_dichiarato} "
                "(atteso se hai escluso delle righe barrate)"
            )
    if not pagina.righe:
        avvisi.append("nessuna riga estratta da questa pagina")
    numeri = [int(r.seq) for r in pagina.righe if r.seq.isdigit()]
    buchi = [f"{a}-{b}" for a, b in zip(numeri, numeri[1:]) if b - a > 1]
    if buchi:
        avvisi.append(f"numeri di riga non consecutivi (fra {', '.join(buchi)}): riga saltata?")
    if pagina.note_pagina:
        avvisi.append(f"note a mano sulla pagina: {pagina.note_pagina}")
    return avvisi


def riga_vuota(numero_pagina: int) -> RigaLavoro:
    """Riga aggiunta a mano: colli arrivati senza documentazione."""
    return RigaLavoro(
        id=uuid.uuid4().hex[:12],
        pagina=numero_pagina,
        magazzino=MAGAZZINO_DEFAULT,
        origine="manuale",
        avvisi=["riga inserita a mano"],
    )
