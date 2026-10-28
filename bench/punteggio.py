"""Confronto fra un'estrazione e l'atteso di un caso del banco di prova.

Le metriche che contano per il carico merci, dalla piu' alla meno grave:

  errore silenzioso   codice o taglie sbagliati SENZA che il checksum
                      `somma(qta) == Total` se ne accorga: finisce nel
                      gestionale se l'operatore non rilegge tutto
  riga perfetta       codice, taglie, barratura e magazzino tutti giusti:
                      l'operatore non deve toccarla
  pagina perfetta     tutte le righe perfette e nessuna in piu' o in meno

I casi di `test_data` (famiglia `test_data`, campo `atteso_carico`) hanno come
atteso il carico, non lo stampato: si valutano con `valuta_carico`, che passa
l'estrazione da `costruisci_righe` come fa l'app. Li' una "riga" e' una taglia.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH.parent))

from bolle.lavoro import costruisci_righe  # noqa: E402
from bolle.schema import PaginaEstratta  # noqa: E402
from bolle.sizes import espandi, uniforma_taglia  # noqa: E402

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


def carica_casi() -> list[dict]:
    """I casi di `importa_test_data.py`, piu' quelli di `genera.py` se ci sono."""
    casi = []
    for nome in ("casi.json", "casi_test_data.json"):
        f = BENCH / "casi" / nome
        if f.exists():
            casi += json.loads(f.read_text(encoding="utf-8"))
    return casi


def righe_attese(caso: dict) -> int:
    """Righe di bolla, o taglie di carico per i casi di test_data."""
    if "atteso_carico" in caso:
        return len(caso["atteso_carico"])
    return len(caso["atteso"]["righe"])


def magazzini_di(annotazione: str) -> list[str]:
    return sorted({f"MAG {n}" for n in _MAG.findall(annotazione or "")})


def valuta(caso: dict, ottenuto: dict | None) -> dict:
    """Esito di un caso. `ottenuto=None` significa estrazione fallita."""
    if "atteso_carico" in caso:
        return valuta_carico(caso, ottenuto)
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


# Avvisi di lavoro.py che mandano la riga tra le "Da controllare": un errore
# su una riga cosi' l'operatore lo vede, quindi non e' silenzioso. Stesse regole
# di gravita() in index.html, tranne la variante da confermare: dipende dal CSV,
# non dalla lettura, e la avrebbero quasi tutte le righe.
_AVVISI_SEGNALATI = ("somma", "totale", "lettura discorde", "non interpretabile",
                     "size/qty vuota", "nessuna coppia", "quantita' non valida",
                     "codice articolo non letto", "piu' magazzini",
                     "magazzino scritto a mano ma illeggibile")


def _segnalata(avvisi: list[str]) -> bool:
    for a in avvisi:
        a = a.lower()
        # il testo del modello dopo "lettura incerta:" non va cercato per parole
        # chiave, ma l'avviso in se' manda la riga tra le "Da controllare"
        if a.startswith("lettura incerta"):
            return True
        if a.startswith(("dal pacco misto", "variante '")):
            continue
        if a.startswith(("corretto a mano", "correzione a mano non applicata",
                         "magazzino a mano non applicato")):
            return True
        if any(k in a for k in _AVVISI_SEGNALATI):
            return True
    return False


def _carico_letto(righe) -> dict[tuple, dict]:
    """Il carico come lo esporterebbe l'app: senza righe escluse, quantita'
    sommate per (codice, taglia, magazzino letto dalla penna)."""
    carico: dict[tuple, dict] = {}
    for r in righe:
        if r.eliminata:
            continue
        mag = r.magazzino if any(a.startswith("magazzino proposto") for a in r.avvisi) else ""
        chiave = (r.codice_articolo.strip().upper(), r.taglia, mag)
        voce = carico.setdefault(chiave, {"qta": 0, "avvisi": []})
        voce["qta"] += r.qta
        voce["avvisi"] += [a for a in r.avvisi if a not in voce["avvisi"]]
    return carico


def _carico_atteso(caso: dict) -> dict[tuple, int]:
    carico: dict[tuple, int] = {}
    for a in caso["atteso_carico"]:
        if a["barrata"]:  # per convenzione non ci sono; se ci fossero, non entrano nel carico
            continue
        # un pacco misto "XS/L" diventa XS + L, come in costruisci_righe
        for t in espandi(a["taglia"], a["qta"]):
            # 910A e 9-10A: la stessa taglia, come la uniforma costruisci_righe
            chiave = (a["codice_articolo"], uniforma_taglia(t.taglia), a["magazzino"])
            carico[chiave] = carico.get(chiave, 0) + t.qta
    return carico


def valuta_carico(caso: dict, ottenuto: dict | None) -> dict:
    """Confronto a livello di carico, come lo vede il gestionale.

    Da entrambe le parti: una voce per (codice, taglia, magazzino), righe
    barrate escluse (il ground truth non le elenca), quantita' sommate come
    nell'export. Il Seq-no non conta. Il magazzino vale come letto solo se viene
    dalla penna (avviso "magazzino proposto"): il default dell'app non e' una
    lettura. Una "riga" qui e' una voce di carico.
    """
    atteso = _carico_atteso(caso)

    e = {k: 0 for k in (
        "codice", "taglie", "totale", "perfette", "silenziosi", "silenziosi_segnalati",
        "incerte", "incerte_a_vuoto", "mag_att", "mag_ok", "mag_inventati",
        "barr_att", "barr_ok", "barr_inventate", "corr_att", "corr_ok", "corr_inventate",
        "parole_att", "parole_ok", "righe_in_piu", "numero_documento", "rotazione",
    )}
    e.update(righe=len(atteso), fallita=ottenuto is None, errori=[])

    letto: dict[tuple, dict] = {}
    if ottenuto is not None:
        try:
            letto = _carico_letto(costruisci_righe(PaginaEstratta.model_validate(ottenuto), 1))
        except Exception as exc:  # fuori schema: per il carico e' come non averla letta
            e["fallita"] = True
            e["errori"].append(f"estrazione non valida: {type(exc).__name__}: {str(exc)[:120]}")
        e["numero_documento"] = int(
            str(ottenuto.get("numero_documento", "")).strip().upper()
            == caso["numero_documento"].strip().upper()
        )

    # abbinamento per (codice, taglia): prima con lo stesso magazzino, poi con
    # uno qualsiasi, cosi' un magazzino sbagliato e' un errore di magazzino e
    # non una voce mancante piu' una in piu'
    liberi = dict(letto)
    abbinati: dict[tuple, tuple | None] = {}
    for chiave in atteso:
        abbinati[chiave] = chiave if chiave in liberi else None
        if abbinati[chiave]:
            del liberi[chiave]
    for (codice, taglia, mag), trovato in abbinati.items():
        if trovato is None:
            altro = next((k for k in liberi if k[:2] == (codice, taglia)), None)
            if altro:
                abbinati[(codice, taglia, mag)] = altro
                del liberi[altro]

    for (codice, taglia, mag), trovato in abbinati.items():
        qta = atteso[(codice, taglia, mag)]
        dove = f"{codice} taglia {taglia}" + (f" {mag}" if mag else "")
        e["mag_att"] += bool(mag)
        if trovato is None:
            e["errori"].append(f"{dove} (qta {qta}) mancante nel carico")
            continue
        voce = letto[trovato]
        ok_qta = voce["qta"] == qta
        ok_mag = trovato[2] == mag

        e["codice"] += 1
        e["taglie"] += ok_qta
        e["totale"] += ok_qta
        e["perfette"] += ok_qta and ok_mag
        if mag:
            e["mag_ok"] += ok_mag
        elif trovato[2]:
            e["mag_inventati"] += 1

        dubbio = any(a.startswith("lettura incerta") for a in voce["avvisi"])
        e["incerte"] += dubbio
        if not ok_qta:
            if not _segnalata(voce["avvisi"]):
                e["silenziosi"] += 1
                e["silenziosi_segnalati"] += dubbio
        elif dubbio:
            e["incerte_a_vuoto"] += 1

        if not ok_qta:
            e["errori"].append(f"{dove} qta: attesa {qta}, letta {voce['qta']}")
        if not ok_mag:
            e["errori"].append(f"{dove} magazzino: atteso {mag or '-'}, letto {trovato[2] or '-'}")

    # una voce in piu' nel carico e' merce che non c'e' (o un codice letto
    # male): errore silenzioso se nessun controllo la segnala
    e["righe_in_piu"] = len(liberi)
    for (codice, taglia, mag), voce in liberi.items():
        e["errori"].append(f"in piu' nel carico: {codice} taglia {taglia} qta {voce['qta']}"
                           + (f" {mag}" if mag else ""))
        segnalata = _segnalata(voce["avvisi"])
        e["silenziosi"] += not segnalata
        e["silenziosi_segnalati"] += not segnalata and any(
            a.startswith("lettura incerta") for a in voce["avvisi"])

    e["pagina_perfetta"] = int(not e["fallita"] and e["perfette"] == e["righe"] and not liberi)
    return e
