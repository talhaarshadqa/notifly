"""Command handlers, independent of python-telegram-bot so they can be tested."""
from __future__ import annotations

import time

from .parse import parse_reminder
from .store import Store

HELP = (
    "\U0001F916 *notifly*\n"
    "/note <text> - save a note\n"
    "/notes - list your notes\n"
    "/delnote <id> - delete a note\n"
    "/remind in <time> <text> - set a reminder (e.g. /remind in 2h call mom)\n"
    "/help - show this message"
)


def handle_command(store: Store, chat_id: int, command: str, args: str, *, now: float | None = None) -> str:
    now = time.time() if now is None else now
    command = command.lstrip("/").lower()

    if command in ("start", "help"):
        return HELP

    if command == "note":
        if not args.strip():
            return "Usage: /note <text>"
        nid = store.add_note(chat_id, args.strip())
        return f"\U0001F4DD Saved note #{nid}."

    if command == "notes":
        notes = store.list_notes(chat_id)
        if not notes:
            return "You have no notes yet. Add one with /note."
        return "\n".join(f"#{n.id}: {n.text}" for n in notes)

    if command == "delnote":
        try:
            nid = int(args.strip())
        except ValueError:
            return "Usage: /delnote <id>"
        return "\U0001F5D1 Deleted." if store.delete_note(chat_id, nid) else "No note with that id."

    if command == "remind":
        try:
            seconds, message = parse_reminder(args)
        except ValueError as exc:
            return str(exc)
        store.add_reminder(chat_id, message, now + seconds)
        mins = seconds // 60
        when = f"{mins} min" if mins else f"{seconds} sec"
        return f"⏰ Okay, I'll remind you in {when}: {message}"

    return "Unknown command. Try /help."
