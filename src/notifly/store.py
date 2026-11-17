"""SQLite storage for notes and reminders, keyed by chat."""
from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    due_at REAL NOT NULL,
    sent INTEGER NOT NULL DEFAULT 0
);
"""


@dataclass
class Note:
    id: int
    text: str


@dataclass
class Reminder:
    id: int
    chat_id: int
    text: str
    due_at: float


class Store:
    def __init__(self, path: str = "notifly.db") -> None:
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)

    # notes
    def add_note(self, chat_id: int, text: str) -> int:
        cur = self.db.execute(
            "INSERT INTO notes (chat_id, text, created_at) VALUES (?, ?, ?)",
            (chat_id, text, time.time()),
        )
        self.db.commit()
        return cur.lastrowid

    def list_notes(self, chat_id: int) -> list[Note]:
        rows = self.db.execute(
            "SELECT id, text FROM notes WHERE chat_id = ? ORDER BY id", (chat_id,)
        ).fetchall()
        return [Note(r["id"], r["text"]) for r in rows]

    def delete_note(self, chat_id: int, note_id: int) -> bool:
        cur = self.db.execute(
            "DELETE FROM notes WHERE chat_id = ? AND id = ?", (chat_id, note_id)
        )
        self.db.commit()
        return cur.rowcount > 0

    # reminders
    def add_reminder(self, chat_id: int, text: str, due_at: float) -> int:
        cur = self.db.execute(
            "INSERT INTO reminders (chat_id, text, due_at) VALUES (?, ?, ?)",
            (chat_id, text, due_at),
        )
        self.db.commit()
        return cur.lastrowid

    def due_reminders(self, now: float | None = None) -> list[Reminder]:
        now = time.time() if now is None else now
        rows = self.db.execute(
            "SELECT id, chat_id, text, due_at FROM reminders WHERE sent = 0 AND due_at <= ?",
            (now,),
        ).fetchall()
        return [Reminder(r["id"], r["chat_id"], r["text"], r["due_at"]) for r in rows]

    def mark_sent(self, reminder_id: int) -> None:
        self.db.execute("UPDATE reminders SET sent = 1 WHERE id = ?", (reminder_id,))
        self.db.commit()

    def close(self) -> None:
        self.db.close()
