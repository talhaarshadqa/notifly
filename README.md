# ⏰ notifly

[![CI](https://github.com/talhaarshadqa/notifly/actions/workflows/ci.yml/badge.svg)](https://github.com/talhaarshadqa/notifly/actions)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Telegram](https://img.shields.io/badge/Telegram-26A5E4?logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

**A Telegram bot for notes and reminders.** Save quick notes and get pinged when a reminder
is due. Built with `python-telegram-bot`, with the command logic kept separate so it's
**fully unit-tested** and backed by SQLite.

## ✨ Features

- **Notes**: `/note buy milk`, `/notes`, `/delnote 3` — stored per chat
- **Reminders**: `/remind in 2h call mom` — natural durations like `10m`, `2h 30m`, `1d`
- **Durable storage** in SQLite, so notes and reminders survive restarts
- **Background checker** delivers reminders when they come due
- Handlers and parsing have **no Telegram dependency** → tested on Python 3.10–3.13

## 🚀 Run it

```bash
git clone https://github.com/talhaarshadqa/notifly.git
cd notifly
pip install -e .
export TELEGRAM_TOKEN="your-bot-token"   # from @BotFather
notifly
```

## 💬 Commands

| Command | Description |
|---|---|
| `/note <text>` | Save a note |
| `/notes` | List your notes |
| `/delnote <id>` | Delete a note |
| `/remind in <time> <text>` | Set a reminder (e.g. `/remind in 90m stretch`) |
| `/help` | Show help |

## 🧠 How it works

Durations are parsed by a small, tested parser (`10m` → 600s, `2h 30m` → 9000s). Reminders
are written to SQLite with a due time; a job runs every 30 seconds, finds due reminders,
sends them, and marks them delivered. Because the parser, storage and command handlers
don't import Telegram, the whole core is tested without a bot token or network.

## 🧪 Development

```bash
pip install -e ".[dev]"
pytest --cov=notifly
```

## 📄 License

MIT
