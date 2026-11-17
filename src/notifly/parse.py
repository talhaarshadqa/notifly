"""Parsing helpers for durations and reminder commands."""
from __future__ import annotations

import re

_DUR = re.compile(r"(\d+)\s*(s|sec|secs|m|min|mins|h|hr|hrs|hour|hours|d|day|days)\b", re.IGNORECASE)
_UNIT = {"s": 1, "sec": 1, "secs": 1, "m": 60, "min": 60, "mins": 60,
         "h": 3600, "hr": 3600, "hrs": 3600, "hour": 3600, "hours": 3600,
         "d": 86400, "day": 86400, "days": 86400}


def parse_duration(text: str) -> int:
    """'10m' -> 600, '2h 30m' -> 9000, '1 day' -> 86400. Returns seconds."""
    total = 0
    found = False
    for num, unit in _DUR.findall(text):
        total += int(num) * _UNIT[unit.lower()]
        found = True
    if not found:
        raise ValueError("couldn't understand the duration (try '10m', '2h', '1d')")
    return total


def parse_reminder(args: str) -> tuple[int, str]:
    """Parse 'in 10m buy milk' or '2h standup' -> (seconds, 'buy milk').

    The leading word 'in' is optional. The duration is taken from the front.
    """
    text = args.strip()
    if text.lower().startswith("in "):
        text = text[3:]
    m = re.match(r"((?:\d+\s*[a-z]+\s*)+)(.*)", text, re.IGNORECASE)
    if not m:
        raise ValueError("usage: /remind in <time> <message>")
    seconds = parse_duration(m.group(1))
    message = m.group(2).strip()
    if not message:
        raise ValueError("what should I remind you about?")
    return seconds, message
