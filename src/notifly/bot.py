"""python-telegram-bot adapter. Imported lazily so the package installs tokenless."""
from __future__ import annotations
import os

from .handlers import handle_command
from .store import Store


def run(token: str | None = None, db_path: str = "notifly.db") -> None:  # pragma: no cover
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

    token = token or os.environ["TELEGRAM_TOKEN"]
    store = Store(db_path)
    app = Application.builder().token(token).build()

    async def on_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        msg = update.effective_message
        command = msg.text.split()[0]
        args = msg.text[len(command):].strip()
        reply = handle_command(store, update.effective_chat.id, command, args)
        await msg.reply_markdown(reply)

    async def check_reminders(ctx: ContextTypes.DEFAULT_TYPE):
        for r in store.due_reminders():
            await ctx.bot.send_message(r.chat_id, f"⏰ Reminder: {r.text}")
            store.mark_sent(r.id)

    for cmd in ("start", "help", "note", "notes", "delnote", "remind"):
        app.add_handler(CommandHandler(cmd, on_command))
    app.job_queue.run_repeating(check_reminders, interval=30)
    app.run_polling()
