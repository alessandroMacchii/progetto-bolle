"""Confronto fra un'estrazione e l'atteso di un caso del banco di prova.

Le metriche che contano per il carico merci, dalla piu' alla meno grave:

  errore silenzioso   codice o taglie sbagliati SENZA che il checksum
                      `somma(qta) == Total` se ne accorga: finisce nel
                      gestionale se l'operatore non rilegge tutto
  riga perfetta       codice, taglie, barratura e magazzino tutti giusti:
                      l'operatore non deve toccarla
  pagina perfetta     tutte le righe perfette e nessuna in piu' o in meno
"""
from __future__ import annotations

import re

# "MAG 1", "mag2", ma anche le abbreviazioni "M1" / "M. 2" che si usano a margine
_MAG = re.compile(r"(?<![A-Za-z0-9])M(?:AG)?\.?\s*(\d)(?![0-9])", re.IGNORECASE)


def taglie_di(riga: dict) -> list[tuple[str, int]]:
    """Coppie (token, qta) ordinate. `XS/L/1` (pacco misto) si taglia sull'ultima barra."""
    coppie = []
    for token in str(riga.get("size_qty_raw") or "").replace("\n", " ").split():
        taglia, _, qta = token.rpartition("/")
        if not taglia or not qta.isdigit():
            coppie = []
            break
        coppie.append((taglia.upper(), int(qta)))
    if not coppie:  # grezzo illeggibile: ripiego sulla scomposizione del modello
        coppie = [
            (str(t.get("taglia", "")).strip().upper(), int(t.get("qta") or 0))
            for t in riga.get("taglie") or []
        ]
    return sorted(coppie)


def correzioni_di(riga: dict) -> set[tuple[str, str, int]]:
    """Correzioni a mano strutturate: (taglia stampata, taglia corretta, qta corretta)."""
    return {
        (
            str(c.get("taglia_stampata", "")).strip().upper(),
            str(c.get("taglia_corretta", "")).strip().upper(),
            int(c.get("qta_corretta", -1)),
        )
        for c in riga.get("correzioni") or []
    }


def magazzini_di(annotazione: str) -> list[str]:
    return sorted({f"MAG {n}" for n in _MAG.findall(annotazione or "")})


def valuta(caso: dict, ottenuto: dict | None) -> dict:
    """Esito di un caso. `ottenuto=None` significa estrazione fallita."""
    atteso = caso["atteso"]
    extra = caso["righe_extra"]
    righe_att = atteso["righe"]
    righe_ott = (ottenuto or {}).get("righe") or []

    e = {
        "righe": len(righe_att),
        "fallita": ottenuto is None,
        "codice": 0, "taglie": 0, "totale": 0, "perfette": 0, "silenziosi": 0,
        "silenziosi_segnalati": 0, "incerte": 0, "incerte_a_vuoto": 0,
        "mag_att": 0, "mag_ok": 0, "mag_inventati": 0,
        "barr_att": 0, "barr_ok": 0, "barr_inventate": 0,
        "corr_att": 0, "corr_ok": 0, "corr_inventate": 0,
        "parole_att": 0, "parole_ok": 0,
        "righe_in_piu": max(0, len(righe_ott) - len(righe_att)),
        "numero_documento": int(
            bool(ottenuto) and str(ottenuto.get("numero_documento", "")).strip().upper()
            == atteso["numero_documento"].upper()
        ),
        "rotazione": int(
            bool(ottenuto) and ottenuto.get("rotazione_gradi") == atteso["rotazione_gradi"]
        ),
        "errori": [],
    }

    for i, att in enumerate(righe_att):
        mag_att = extra[i]["mag"]
        parole = extra[i]["parole"]
        e["mag_att"] += bool(mag_att)
        e["barr_att"] += att["barrata"]
        e["parole_att"] += len(parole)
        if i >= len(righe_ott):
            e["errori"].append(f"riga {att['seq'] or i + 1} ({att['codice_articolo']}) mancante")
            continue
        ott = righe_ott[i]
        nota = str(ott.get("annotazioni_manoscritte") or "")

        ammessi = extra[i].get("codici") or [att["codice_articolo"]]
        ok_codice = str(ott.get("codice_articolo", "")).strip().upper() in [c.upper() for c in ammessi]
        ok_taglie = taglie_di(ott) == taglie_di(att)
        ok_totale = ott.get("totale_dichiarato") == att["totale_dichiarato"]
        ok_barr = bool(ott.get("barrata")) == att["barrata"]
        mag_ott = magazzini_di(nota)
        if not mag_ott and not ott.get("barrata"):  # come fa l'app: vale la sigla di pagina
            mag_ott = magazzini_di((ottenuto or {}).get("magazzino_pagina") or "")
        ok_mag = mag_ott == mag_att

        e["codice"] += ok_codice
        e["taglie"] += ok_taglie
        e["totale"] += ok_totale
        e["perfette"] += ok_codice and ok_taglie and ok_barr and ok_mag
        if mag_att:
            e["mag_ok"] += ok_mag
        elif mag_ott:
            e["mag_inventati"] += 1
        if att["barrata"]:
            e["barr_ok"] += ok_barr
        elif ott.get("barrata"):
            e["barr_inventate"] += 1
        e["parole_ok"] += sum(p.upper() in nota.upper() for p in parole)

        corr_att, corr_ott = correzioni_di(att), correzioni_di(ott)
        e["corr_att"] += len(corr_att)
        e["corr_ok"] += len(corr_att & corr_ott)
        e["corr_inventate"] += len(corr_ott - corr_att)

        quadra = sum(q for _, q in taglie_di(ott)) == ott.get("totale_dichiarato")
        dubbio = bool(str(ott.get("incertezze") or "").strip())
        e["incerte"] += dubbio
        if not ok_codice or (not ok_taglie and quadra):
            e["silenziosi"] += 1
            # il modello ha detto "qui non sono sicuro": l'operatore lo vede
            e["silenziosi_segnalati"] += dubbio
        elif dubbio:
            e["incerte_a_vuoto"] += 1

        dove = f"riga {att['seq'] or i + 1}"
        if not ok_codice:
            e["errori"].append(f"{dove} codice: atteso {att['codice_articolo']}, letto {ott.get('codice_articolo')!r}")
        if not ok_taglie:
            e["errori"].append(f"{dove} taglie: atteso {att['size_qty_raw']!r}, letto {ott.get('size_qty_raw')!r}")
        if not ok_barr:
            e["errori"].append(f"{dove} barrata: atteso {att['barrata']}, letto {bool(ott.get('barrata'))}")
        if not ok_mag:
            e["errori"].append(f"{dove} magazzino: atteso {mag_att or '-'}, letto {mag_ott or '-'} ({nota!r})")
        if corr_att != corr_ott:
            e["errori"].append(f"{dove} correzioni: attese {sorted(corr_att)}, lette {sorted(corr_ott)}")

    e["pagina_perfetta"] = int(
        not e["fallita"] and e["perfette"] == e["righe"] and len(righe_ott) == len(righe_att)
    )
    return e
