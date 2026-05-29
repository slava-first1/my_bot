from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from openai import OpenAI
from config.states import HAVAL


async def haval_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="что ты ел сегодня ?",
    )

    return HAVAL


async def haval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.lower()
    client = OpenAI()

    lst = [
        {
            "role": "developer",
            "content": "отвечай сколько белков моей еде только одним числом",
        }
    ] + [
        {"role": "user", "content": text},
    ]

    response = client.responses.create(
        model="gpt-5.4-nano",
        reasoning={"effort": "low"},
        input=lst,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"тут {response.output_text} белков\nЕще что-то ел?"
    )
    context.user_data["total_protein"] = context.user_data["total_protein"] + int(response.output_text)
    

    return HAVAL


async def total_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_protein = context.user_data["total_protein"]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"сегодня ты съел {total_protein} белков ",
    )


async def new_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["total_protein"] = 0
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"новый день! у вса снова 0 белков"
    )
