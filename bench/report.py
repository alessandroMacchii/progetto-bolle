"""Tabelle di confronto fra i modelli provati: `bench/REPORT.md`.

    python bench/report.py            # tutti i risultati in bench/risultati/
    python bench/report.py --errori   # in piu', l'elenco degli errori caso per caso
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))

from punteggio import carica_casi, righe_attese, valuta  # noqa: E402

SOMMABILI = [
    "righe", "codice", "taglie", "perfette", "silenziosi", "mag_att", "mag_ok", "mag_inventati",
    "barr_att", "barr_ok", "barr_inventate", "corr_att", "corr_ok", "corr_inventate",
    "parole_att", "parole_ok", "righe_in_piu",
    "numero_documento", "rotazione", "pagina_perfetta", "fallita",
    "silenziosi_segnalati", "incerte", "incerte_a_vuoto",
]


def pct(a: int, b: int) -> str:
    return f"{100 * a / b:.0f}%" if b else "-"


def somma(esiti: list[dict]) -> dict:
    tot = {k: sum(int(e[k]) for e in esiti) for k in SOMMABILI}
    tot["pagine"] = len(esiti)
    return tot


def riga_tabella(nome: str, t: dict, costo: str = "", tempo: str = "") -> str:
    celle = [
        nome,
        f"{t['pagina_perfetta']}/{t['pagine']}",
        pct(t["perfette"], t["righe"]),
        pct(t["codice"], t["righe"]),
        pct(t["taglie"], t["righe"]),
        f"{t['mag_ok']}/{t['mag_att']}" + (f" (+{t['mag_inventati']} inventati)" if t["mag_inventati"] else ""),
        f"{t['barr_ok']}/{t['barr_att']}" + (f" (+{t['barr_inventate']} inventate)" if t["barr_inventate"] else ""),
        f"{t['corr_ok']}/{t['corr_att']}" + (f" (+{t['corr_inventate']} inventate)" if t["corr_inventate"] else ""),
        str(t["silenziosi"]),
        str(t["silenziosi"] - t["silenziosi_segnalati"]),
        f"{t['incerte']} ({t['incerte_a_vuoto']} a vuoto)",
        costo,
        tempo,
    ]
    return "| " + " | ".join(celle) + " |"


TESTATA = (
    "| {} | pagine perfette | righe perfette | codice | taglie | magazzino | barrate | correzioni a mano | "
    "errori silenziosi | di cui NON segnalati | righe segnalate incerte | costo/pagina | sec/pagina |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|---|---|"
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--errori", action="store_true")
    ap.add_argument("--modelli", default="", help="solo i modelli il cui nome contiene una di queste parole (a,b)")
    ap.add_argument("--comuni", action="store_true", help="solo i casi letti da TUTTI i modelli scelti")
    ap.add_argument("--prompt", action="store_true", help="in coda, il testo dei prompt v1 e v2")
    ap.add_argument("--uscita", default="REPORT.md")
    args = ap.parse_args()

    casi = carica_casi()
    per_id = {c["id"]: c for c in casi}
    fuori = ["# Confronto modelli sul banco di prova", ""]
    fuori.append(
        f"{len(casi)} casi: "
        + " e ".join(x for x in (
            f"{sum(righe_attese(c) for c in casi if 'atteso' in c)} righe di bolla"
            if any("atteso" in c for c in casi) else "",
            f"{sum(righe_attese(c) for c in casi if 'atteso_carico' in c)} taglie di carico"
            if any("atteso_carico" in c for c in casi) else "",
        ) if x)
        + ". Generato da `python bench/report.py`."
    )

    modelli = {}
    for f in sorted((BENCH / "risultati").glob("*.json")):
        dati = json.loads(f.read_text(encoding="utf-8"))
        esiti = {
            cid: valuta(per_id[cid], voce.get("output"))
            for cid, voce in dati["casi"].items()
            if cid in per_id
        }
        filtri = [x for x in args.modelli.split(",") if x]
        if filtri and not any(x in dati["modello"] for x in filtri):
            continue
        modelli[dati["modello"]] = (dati, esiti)

    if args.comuni and modelli:
        comuni = set.intersection(*(set(e) for _, e in modelli.values()))
        modelli = {n: (d, {i: v for i, v in e.items() if i in comuni}) for n, (d, e) in modelli.items()}
        casi = [c for c in casi if c["id"] in comuni]
        fuori[-1] = f"Confronto ristretto ai {len(casi)} casi letti da tutti i modelli elencati."

    def costo_tempo(dati, ids):
        voci = [dati["casi"][i] for i in ids]
        costi = [v["costo_usd"] for v in voci if v.get("costo_usd") is not None]
        tempi = [v["secondi"] for v in voci if v.get("secondi")]
        return (
            f"${sum(costi) / len(costi):.4f}" if costi else "n.d.",
            f"{sum(tempi) / len(tempi):.0f}" if tempi else "n.d.",
        )

    # i casi di test_data contano le taglie, non le righe di bolla: sommarli
    # ai casi di genera.py mescolerebbe due unita' di misura
    di_bolla = [c["id"] for c in casi if "atteso" in c] or [c["id"] for c in casi]
    misti = len(di_bolla) < len(casi)
    fuori += ["", "## Complessivo" + (" (senza test_data)" if misti else ""), "", TESTATA.format("modello")]
    for nome, (dati, esiti) in modelli.items():
        ids = [i for i in esiti if i in di_bolla]
        if not ids:
            continue
        completo = "" if len(ids) == len(di_bolla) else f" ({len(ids)} casi su {len(di_bolla)})"
        fuori.append(riga_tabella(nome + completo, somma([esiti[i] for i in ids]), *costo_tempo(dati, ids)))

    for famiglia, titolo in [
        ("reale", "Calligrafia vera (14 pagine di esempio)"),
        ("pulita", "Bolle bianche (altrebolle/)"),
        ("sintetica", "Varianti con annotazioni disegnate"),
        ("test_data", "Ground truth di test_data (confronto sul carico: una riga per taglia)"),
    ]:
        if not misti or not any(c["famiglia"] == famiglia for c in casi):
            continue  # con una famiglia sola la tabella ripeterebbe il complessivo
        fuori += ["", f"## {titolo}", "", TESTATA.format("modello")]
        for nome, (dati, esiti) in modelli.items():
            ids = [i for i in esiti if per_id[i]["famiglia"] == famiglia]
            if ids:
                fuori.append(riga_tabella(nome, somma([esiti[i] for i in ids])))

    fuori += ["", "## Caso per caso (righe perfette / righe)", ""]
    fuori.append("| caso | cosa prova | " + " | ".join(modelli) + " |")
    fuori.append("|---|---|" + "---|" * len(modelli))
    for c in casi:
        celle = []
        for _nome, (_dati, esiti) in modelli.items():
            e = esiti.get(c["id"])
            if e is None:
                celle.append("")
            elif e["fallita"]:
                celle.append("FALLITA")
            else:
                celle.append(f"{e['perfette']}/{e['righe']}" + (" ⚠" if e["silenziosi"] else ""))
        fuori.append(f"| {c['id']} | {c['descrizione']} | " + " | ".join(celle) + " |")
    fuori += ["", "⚠ = almeno un errore silenzioso (non intercettato dal checksum)."]

    for nome, (dati, _) in modelli.items():
        if dati.get("nota"):
            fuori.append(f"\n- **{nome}**: {dati['nota']}")
        motori = [v["motore"] for v in dati["casi"].values() if v.get("motore")]
        if motori:  # consenso: quante pagine ha dovuto rileggere l'arbitro
            arbitrate = [m for m in motori if not m.endswith("concordi")]
            fuori.append(f"  Pagine passate all'arbitro: {len(arbitrate)} su {len(motori)}.")

    if args.errori:
        fuori += ["", "## Errori"]
        for nome, (_dati, esiti) in modelli.items():
            fuori += ["", f"### {nome}", ""]
            for cid, e in esiti.items():
                if e["fallita"]:
                    fuori.append(f"- `{cid}`: estrazione fallita")
                for err in e["errori"]:
                    fuori.append(f"- `{cid}`: {err}")

    if args.prompt:
        sys.path.insert(0, str(BENCH.parent))
        from bolle.extract import ISTRUZIONI

        v1 = (BENCH / "prompt_v1.txt").read_text(encoding="utf-8")
        fuori += [
            "", "## I due prompt", "",
            "Con il v1 lo schema di uscita non ha i campi `incertezze`, `codice_manoscritto`, "
            "`magazzino_pagina` e `note_pagina` (`bench/schema_v1.json`); il v2 e' quello "
            "dell'applicazione (`bolle/extract.py`, `bolle/schema.py`).",
            "", "### Prompt v1", "", "```text", v1.strip(), "```",
            "", "### Prompt v2", "", "```text", ISTRUZIONI.strip(), "```",
        ]

    testo = "\n".join(fuori) + "\n"
    (BENCH / args.uscita).write_text(testo, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(testo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
