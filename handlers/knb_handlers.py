import random
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from config.states import KNB 

async def knb_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['бумага'], ['ножницы'],['камень']]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ты попал в игру. Напиши камень, ножницы или бумага",
        reply_markup=markup
    )
    return KNB


async def knb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.lower()

    variantu = [
        "камень",
        "ножницы",
        "бумага",
    ]

    if text in variantu:
        bot_var = random.choice(variantu)

        if text == bot_var:
            result = "Ничья!"
        elif (
            (text == "камень" and bot_var == "ножницы")
            or (text == "ножницы" and bot_var == "бумага")
            or (text == "бумага" and bot_var == "камень")
        ):
            result = "Ты выиграл!"
        else:
            result = "Ты проиграл!"

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"бот-{bot_var},\n{result}"
        )
    elif text == "подвал":
        result = "тебя скелет поцеловал"
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{result}"
        )

    elif text == "привет":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет")

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Напиши камень, ножницы,  бумага или подвал",
        )