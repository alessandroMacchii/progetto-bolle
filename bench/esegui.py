"""Fa leggere i casi del banco di prova a un modello e salva le risposte.

    python bench/esegui.py --modello sonnet-5.5
    python bench/esegui.py --modello gemini-flash --casi reale        # solo una famiglia
    python bench/esegui.py --modello locale-qwen3.5-0.8b --limite 5
    python bench/esegui.py --importa cartella/ --modello nome         # JSON gia' pronti

I modelli stanno in `bench/modelli.json`. Chiavi necessarie (in `.env`):

    anthropic    ANTHROPIC_API_KEY
    openrouter   OPENROUTER_API_KEY   (una chiave sola per Gemini, GPT, Qwen, ...)
    ollama       nessuna: gira sul PC

Prompt e schema sono quelli dell'applicazione (`bolle/extract.py`,
`bolle/schema.py`): si misura il software vero, non una sua copia. Le risposte
gia' salvate non vengono richieste di nuovo, quindi il comando si puo'
rilanciare dopo un'interruzione senza pagare due volte.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE))

from bolle.extract import ISTRUZIONI, schema_stretto as _schema_stretto  # noqa: E402  (carica anche .env)
from bolle.schema import PaginaEstratta  # noqa: E402

BENCH = RADICE / "bench"
RISULTATI = BENCH / "risultati"
DOMANDA = "Estrai i dati di questa pagina."


def _b64(jpg: Path) -> str:
    return base64.standard_b64encode(jpg.read_bytes()).decode("ascii")


def _post(url: str, corpo: dict, intestazioni: dict, timeout: int = 900) -> dict:
    richiesta = urllib.request.Request(
        url,
        data=json.dumps(corpo).encode("utf-8"),
        headers={"Content-Type": "application/json", **intestazioni},
    )
    try:
        with urllib.request.urlopen(richiesta, timeout=timeout) as risposta:
            return json.loads(risposta.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:400]}") from exc


# --- fornitori: ognuno ritorna (dict estratto, token_in, token_out, costo|None) ---

def chiama_anthropic(conf: dict, jpg: Path):
    import anthropic

    parametri = {}
    if conf.get("effort"):
        parametri["output_config"] = {"effort": conf["effort"]}
    r = anthropic.Anthropic().messages.parse(
        model=conf["id"],
        max_tokens=16000,
        system=ISTRUZIONI,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": _b64(jpg)}},
                    {"type": "text", "text": DOMANDA},
                ],
            }
        ],
        output_format=PaginaEstratta,
        **parametri,
    )
    if r.stop_reason == "refusal":
        raise RuntimeError("il modello ha rifiutato la pagina")
    return r.parsed_output.model_dump(), r.usage.input_tokens, r.usage.output_tokens, None


def chiama_openrouter(conf: dict, jpg: Path):
    chiave = os.getenv("OPENROUTER_API_KEY")
    if not chiave:
        raise SystemExit("Manca OPENROUTER_API_KEY in .env (https://openrouter.ai/keys)")
    r = _post(
        "https://openrouter.ai/api/v1/chat/completions",
        {
            "model": conf["id"],
            "messages": [
                {"role": "system", "content": ISTRUZIONI},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_b64(jpg)}"}},
                        {"type": "text", "text": DOMANDA},
                    ],
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": "pagina", "strict": True, "schema": _schema_stretto()},
            },
            "usage": {"include": True},
            "provider": {"require_parameters": True},
        },
        {"Authorization": f"Bearer {chiave}"},
    )
    if "error" in r:
        raise RuntimeError(str(r["error"])[:400])
    uso = r.get("usage") or {}
    dati = json.loads(r["choices"][0]["message"]["content"])
    return dati, uso.get("prompt_tokens", 0), uso.get("completion_tokens", 0), uso.get("cost")


def chiama_ollama(conf: dict, jpg: Path):
    r = _post(
        os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434") + "/api/chat",
        {
            "model": conf["id"],
            "stream": False,
            "think": False,
            "format": _schema_stretto(),
            "options": {"temperature": 0, "num_ctx": 8192},
            "messages": [
                {"role": "system", "content": ISTRUZIONI},
                {"role": "user", "content": DOMANDA, "images": [_b64(jpg)]},
            ],
        },
        {},
        timeout=1800,
    )
    dati = json.loads(r["message"]["content"])
    return dati, r.get("prompt_eval_count", 0), r.get("eval_count", 0), 0.0


FORNITORI = {"anthropic": chiama_anthropic, "openrouter": chiama_openrouter, "ollama": chiama_ollama}


def _carica_modelli() -> dict:
    return json.loads((BENCH / "modelli.json").read_text(encoding="utf-8"))["modelli"]


def _salva(percorso: Path, dati: dict) -> None:
    percorso.parent.mkdir(parents=True, exist_ok=True)
    percorso.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")


# Senza una chiamata API vera i token non si misurano: si stimano. Ingresso =
# immagine da 1600 px (~2400 token) + istruzioni e schema (~1800); uscita = il
# JSON prodotto a ~3 caratteri per token. Il ragionamento del modello, che si
# paga come uscita, NON e' incluso: il costo vero sara' piu' alto.
TOKEN_INGRESSO_STIMATI = 4200


def importa(cartella: Path, nome: str, mappa: Path | None, nota: str, listino: str) -> None:
    """Risposte prodotte fuori da qui: un `<id caso>.json` per pagina."""
    rinomina = json.loads(mappa.read_text(encoding="utf-8")) if mappa else {}
    prezzo = _carica_modelli()[listino]["prezzo"] if listino else None
    casi = {}
    for f in sorted(cartella.glob("*.json")):
        try:
            dati = json.loads(f.read_text(encoding="utf-8"))
            PaginaEstratta.model_validate(dati)
            voce = {"output": dati}
            if prezzo:
                t_out = len(json.dumps(dati, ensure_ascii=False)) // 3
                voce.update(token_in=TOKEN_INGRESSO_STIMATI, token_out=t_out,
                            costo_usd=(TOKEN_INGRESSO_STIMATI * prezzo[0] + t_out * prezzo[1]) / 1e6)
        except Exception as exc:  # JSON rotto o fuori schema: e' un fallimento del modello
            voce = {"output": None, "errore": f"{type(exc).__name__}: {str(exc)[:200]}"}
        casi[rinomina.get(f.stem, f.stem)] = voce
    _salva(RISULTATI / f"{nome}.json", {"modello": nome, "nota": nota, "casi": casi})
    print(f"{nome}: importati {len(casi)} casi")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modello", required=True)
    ap.add_argument("--casi", default="", help="filtro sull'id del caso, es. 'reale' o 'sint-P2'")
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--prompt", default="", choices=["", "v1", "v2", "v3"],
                    help="v1 = prompt e schema della prima prova (bench/prompt_v1.txt); "
                    "v2 = bench/prompt_v2.txt, schema attuale; v3 = quelli "
                    "dell'applicazione. Finisce nel nome del risultato")
    ap.add_argument("--importa", default="", help="cartella di JSON gia' pronti")
    ap.add_argument("--mappa", default="", help="con --importa: JSON {nome file: id caso}")
    ap.add_argument("--nota", default="")
    ap.add_argument("--listino", default="", help="con --importa: modello di modelli.json da cui stimare il costo")
    args = ap.parse_args()

    if args.importa:
        importa(Path(args.importa), args.modello, Path(args.mappa) if args.mappa else None, args.nota,
                args.listino)
        return 0

    modelli = _carica_modelli()
    if args.modello not in modelli:
        print(f"modello sconosciuto. Disponibili: {', '.join(modelli)}")
        return 1
    conf = modelli[args.modello]
    chiama = FORNITORI[conf["fornitore"]]
    nome = f"{args.modello} prompt {args.prompt}" if args.prompt else args.modello
    if args.prompt == "v1":
        # la prima versione: istruzioni piu' corte e schema senza i campi
        # incertezze, codice_manoscritto, magazzino_pagina, note_pagina
        global ISTRUZIONI, _schema_stretto
        ISTRUZIONI = (BENCH / "prompt_v1.txt").read_text(encoding="utf-8")
        schema_v1 = json.loads((BENCH / "schema_v1.json").read_text(encoding="utf-8"))
        _schema_stretto = lambda: schema_v1  # noqa: E731
    elif args.prompt == "v2":
        ISTRUZIONI = (BENCH / "prompt_v2.txt").read_text(encoding="utf-8")

    casi = json.loads((BENCH / "casi" / "casi.json").read_text(encoding="utf-8"))
    casi = [c for c in casi if args.casi in c["id"]]
    if args.limite:
        casi = casi[: args.limite]

    percorso = RISULTATI / f"{nome}.json"
    stato = (
        json.loads(percorso.read_text(encoding="utf-8"))
        if percorso.exists()
        else {"modello": nome, "nota": args.nota, "casi": {}}
    )

    for caso in casi:
        fatto = stato["casi"].get(caso["id"])
        if fatto and fatto.get("output") is not None:
            continue
        inizio = time.time()
        voce: dict = {"output": None}
        try:
            dati, t_in, t_out, costo = chiama(conf, BENCH / "casi" / caso["immagine"])
            PaginaEstratta.model_validate(dati)
            if costo is None and conf.get("prezzo"):
                costo = (t_in * conf["prezzo"][0] + t_out * conf["prezzo"][1]) / 1e6
            voce = {"output": dati, "token_in": t_in, "token_out": t_out, "costo_usd": costo}
        except SystemExit:
            raise
        except Exception as exc:
            voce["errore"] = f"{type(exc).__name__}: {str(exc)[:300]}"
        voce["secondi"] = round(time.time() - inizio, 1)
        stato["casi"][caso["id"]] = voce
        _salva(percorso, stato)
        esito = "ok " if voce["output"] is not None else "ERR"
        print(f"{esito} {caso['id']:32} {voce['secondi']:6.1f}s  {voce.get('errore', '')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
