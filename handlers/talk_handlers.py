from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from config.states import TALK 
async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="привет, как у тебя дела?",
    )
    return TALK

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.lower()

    await update.message.reply_text(f"О, у меня тоже {text}!")
