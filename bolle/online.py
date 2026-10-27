"""Prova online dal PC: l'app gira qui, Cloudflare la rende raggiungibile da un link.

    python -m bolle.online        (oppure "Avvia prova online.bat")

Usa un "quick tunnel" di Cloudflare: gratis e senza account, ma il link
(https://<parole-a-caso>.trycloudflare.com) cambia a ogni avvio e funziona solo
finche' questo PC e' acceso e la finestra resta aperta. Per la prova di qualche
giorno basta; per l'uso vero serve un hosting (vedi README).

Il server ascolta solo su 127.0.0.1: dall'esterno si entra soltanto dal tunnel,
e il tunnel chiede utente e password.
"""
from __future__ import annotations

import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import urllib.request
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
PORTA = 8000
STRUMENTI = ROOT / "strumenti"
CLOUDFLARED_URL = (
    "https://github.com/cloudflare/cloudflared/releases/latest/download/"
    "cloudflared-windows-amd64.exe"
)


def _password() -> str:
    """Quella di .env; se manca la crea e la salva, cosi' resta la stessa fra un avvio e l'altro."""
    env = ROOT / ".env"
    esistente = os.getenv("BOLLE_PASSWORD") or (
        dotenv_values(env).get("BOLLE_PASSWORD") if env.exists() else ""
    )
    if esistente:
        return esistente
    nuova = "-".join(secrets.token_hex(2) for _ in range(3))  # es. 3f1a-90bc-7e22
    testo = env.read_text(encoding="utf-8") if env.exists() else ""
    if testo and not testo.endswith("\n"):
        testo += "\n"
    testo += f"\n# Password della prova online\nBOLLE_PASSWORD={nuova}\n"
    env.write_text(testo, encoding="utf-8")
    return nuova


def _cloudflared() -> str:
    trovato = shutil.which("cloudflared")
    if trovato:
        return trovato
    locale = STRUMENTI / "cloudflared.exe"
    if not locale.exists():
        print("  Scarico cloudflared (una volta sola, ~60 MB)...", flush=True)
        STRUMENTI.mkdir(exist_ok=True)
        parziale = locale.with_suffix(".part")
        urllib.request.urlretrieve(CLOUDFLARED_URL, parziale)
        parziale.replace(locale)
    return str(locale)


def _server() -> None:
    import uvicorn

    from .app import api

    uvicorn.run(api, host="127.0.0.1", port=PORTA, log_level="warning")


def main() -> int:
    print("\n  CARICO MERCI - prova online\n  ===========================\n")
    # va decisa prima di importare la configurazione dell'app, che la legge una volta
    password = _password()
    os.environ["BOLLE_PASSWORD"] = password
    # davanti c'e' Cloudflare: l'indirizzo vero di chi tenta il login sta qui
    os.environ["BOLLE_IP_HEADER"] = "cf-connecting-ip"
    from .config import ACCESSO_UTENTE, EXTRACTOR_BACKEND

    if EXTRACTOR_BACKEND == "mock":
        print("  [!] Motore 'mock': chi apre il link vedra' solo le righe di esempio,")
        print("      non la lettura vera delle bolle. Controlla BOLLE_EXTRACTOR in .env.\n")

    threading.Thread(target=_server, daemon=True).start()

    tunnel = subprocess.Popen(
        [_cloudflared(), "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{PORTA}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    indirizzo = None
    try:
        for riga in tunnel.stdout:
            if indirizzo is None:
                trovato = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", riga)
                if trovato:
                    indirizzo = trovato.group(0)
                    print("  Online. Da mandare a chi prova:\n")
                    print(f"    Link:      {indirizzo}")
                    print(f"    Utente:    {ACCESSO_UTENTE}")
                    print(f"    Password:  {password}\n")
                    print("  Il link vale finche' questa finestra resta aperta e il PC acceso.")
                    print("  Se lo chiudi e lo riapri, il link cambia: va rimandato.")
                    print("  PER CHIUDERE: Ctrl+C qui dentro, oppure chiudi la finestra.\n", flush=True)
                elif " ERR " in riga:
                    print("  " + riga.strip(), flush=True)
            # "Failed to fetch features" e' un controllo opzionale: il tunnel va lo stesso
            elif " ERR " in riga and "Failed to fetch features" not in riga:
                print("  [tunnel] " + riga.strip(), flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        tunnel.terminate()
    if indirizzo is None:
        print("  [X] Il tunnel non e' partito. Controlla la connessione e riprova.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
