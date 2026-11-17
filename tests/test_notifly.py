import pytest

from notifly.handlers import handle_command
from notifly.parse import parse_duration, parse_reminder
from notifly.store import Store


@pytest.fixture
def store():
    s = Store(":memory:")
    yield s
    s.close()


@pytest.mark.parametrize("text,secs", [
    ("10m", 600), ("2h", 7200), ("1d", 86400),
    ("2h 30m", 9000), ("45 sec", 45), ("3 days", 259200),
])
def test_parse_duration(text, secs):
    assert parse_duration(text) == secs


def test_parse_duration_bad():
    with pytest.raises(ValueError):
        parse_duration("soon")


def test_parse_reminder():
    assert parse_reminder("in 10m buy milk") == (600, "buy milk")
    assert parse_reminder("2h standup meeting") == (7200, "standup meeting")
    with pytest.raises(ValueError):
        parse_reminder("in 10m")           # no message
    with pytest.raises(ValueError):
        parse_reminder("buy milk")         # no time


def test_notes_flow(store):
    assert "no notes" in handle_command(store, 1, "/notes", "")
    assert "#1" in handle_command(store, 1, "/note", "buy milk")
    handle_command(store, 1, "/note", "call bank")
    listing = handle_command(store, 1, "/notes", "")
    assert "buy milk" in listing and "call bank" in listing
    # notes are per-chat
    assert "no notes" in handle_command(store, 999, "/notes", "")
    assert "Deleted" in handle_command(store, 1, "/delnote", "1")
    assert "No note" in handle_command(store, 1, "/delnote", "1")
    assert handle_command(store, 1, "/delnote", "x").startswith("Usage")


def test_reminder_flow(store):
    out = handle_command(store, 5, "/remind", "in 2h call mom", now=1000.0)
    assert "call mom" in out
    # not due yet
    assert store.due_reminders(now=1000.0) == []
    # due after 2h
    due = store.due_reminders(now=1000.0 + 7200)
    assert len(due) == 1 and due[0].text == "call mom"
    store.mark_sent(due[0].id)
    assert store.due_reminders(now=1000.0 + 7200) == []


def test_help_and_unknown(store):
    assert "notifly" in handle_command(store, 1, "/start", "")
    assert "Unknown" in handle_command(store, 1, "/frobnicate", "")
    assert handle_command(store, 1, "/note", "").startswith("Usage")
