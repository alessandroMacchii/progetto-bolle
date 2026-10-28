"""Persistenza dei documenti in lavorazione.

Un documento = una bolla caricata, con le sue pagine e le sue righe di lavoro.
Lo stato e' un blob JSON: il prototipo non ha bisogno di query relazionali, e
tenerlo in un solo campo rende banale rileggere una bolla di due mesi fa nello
stato esatto in cui e' stata esportata (tracciabilita' di quello che e' finito
in gestionale).
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any

from .config import DB_PATH

_SCHEMA = """
CREATE TABLE IF NOT EXISTS documenti (
    id          TEXT PRIMARY KEY,
    nome        TEXT NOT NULL,
    creato_il   TEXT NOT NULL,
    aggiornato  TEXT NOT NULL,
    esportato   TEXT NOT NULL DEFAULT '',
    stato       TEXT NOT NULL
);
"""


# Le colonne della tabella: il resto del documento (pagine, righe, operatore,
# storico delle modifiche) sta nel JSON di `stato`.
COLONNE = ("id", "nome", "creato_il", "aggiornato", "esportato")


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(_SCHEMA)
    return conn


def _ora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def nuovo_id() -> str:
    return uuid.uuid4().hex[:12]


def crea(doc_id: str, nome: str, stato: dict[str, Any]) -> None:
    ora = _ora()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO documenti (id, nome, creato_il, aggiornato, stato) "
            "VALUES (?, ?, ?, ?, ?)",
            (doc_id, nome, ora, ora, json.dumps(stato, ensure_ascii=False)),
        )


def salva(doc_id: str, stato: dict[str, Any]) -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE documenti SET stato = ?, aggiornato = ? WHERE id = ?",
            (json.dumps(stato, ensure_ascii=False), _ora(), doc_id),
        )


def segna_esportato(doc_id: str) -> None:
    with _conn() as conn:
        conn.execute("UPDATE documenti SET esportato = ? WHERE id = ?", (_ora(), doc_id))


def carica(doc_id: str) -> dict[str, Any] | None:
    with _conn() as conn:
        row = conn.execute("SELECT * FROM documenti WHERE id = ?", (doc_id,)).fetchone()
    if row is None:
        return None
    return {
        "id": row["id"],
        "nome": row["nome"],
        "creato_il": row["creato_il"],
        "aggiornato": row["aggiornato"],
        "esportato": row["esportato"],
        **json.loads(row["stato"]),
    }


def elenca() -> list[dict[str, Any]]:
    with _conn() as conn:
        righe = conn.execute(
            "SELECT id, nome, creato_il, aggiornato, esportato, stato "
            "FROM documenti ORDER BY creato_il DESC"
        ).fetchall()
    fuori = []
    for r in righe:
        stato = json.loads(r["stato"])
        fuori.append(
            {
                "id": r["id"],
                "nome": r["nome"],
                "creato_il": r["creato_il"],
                "aggiornato": r["aggiornato"],
                "esportato": r["esportato"],
                "pagine": len(stato.get("pagine", [])),
                "righe": sum(1 for x in stato.get("righe", []) if not x.get("eliminata")),
                "in_lettura": bool(stato.get("in_lettura")),
                "operatore": stato.get("operatore", ""),
            }
        )
    return fuori
