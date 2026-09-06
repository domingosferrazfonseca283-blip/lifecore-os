#!/usr/bin/env python3

import os
import sqlite3
from datetime import datetime

LIFECORE_ROOT = os.path.expanduser("~/lifecore")
DATABASE = os.path.join(
    LIFECORE_ROOT,
    "memory",
    "lifecore.db"
)


def connect():
    os.makedirs(
        os.path.dirname(DATABASE),
        exist_ok=True
    )
    return sqlite3.connect(DATABASE)


def initialize():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                bateria REAL,
                temperatura REAL,
                estado TEXT
            )
        """)
        db.commit()


def record(state):
    initialize()
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    with connect() as db:
        db.execute(
            """
            INSERT INTO history (
                timestamp,
                bateria,
                temperatura,
                estado
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                timestamp,
                state.get("bateria"),
                state.get("temperatura"),
                state.get("estado")
            )
        )
        db.commit()


def recent(limit=10):
    initialize()
    with connect() as db:
        cursor = db.execute(
            """
            SELECT
                timestamp,
                bateria,
                temperatura,
                estado
            FROM history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )
        return cursor.fetchall()


def show_history(limit=10):
    rows = recent(limit)

    print()
    print("📈 HISTÓRICO TEMPORAL LIFECORE V1.3")
    print("===================================")

    if not rows:
        print("Nenhum registro temporal.")
    else:
        for timestamp, bateria, temperatura, estado in reversed(rows):
            print(
                f"[{timestamp}] "
                f"bateria={bateria}% | "
                f"temp={temperatura}°C | "
                f"estado={estado}"
            )

    print("===================================")


if __name__ == "__main__":
    show_history()
