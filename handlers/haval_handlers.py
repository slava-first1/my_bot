from telegram import Update
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from openai import OpenAI
from config.states import HAVAL


async def haval_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['/New_day'], ["/Total"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="что ты ел сегодня ?",
        reply_markup=markup,
    )

    return HAVAL


async def haval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.lower()
    client = OpenAI()

    lst = [
        {
            "role": "developer",
            "content":""" "отвечай сколько КБЖУ моей еде только числами в формате:"
             калорий: N
             белки: N
             жиры: N
             углеводы: N
             """
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
        chat_id=update.effective_chat.id, text=  f"{response.output_text}"
    )
    context.user_data.setdefault("total_calories", 0)
    context.user_data.setdefault("total_protein", 0)
    context.user_data.setdefault("total_fat", 0)
    context.user_data.setdefault("total_carbs", 0)
    lines = response.output_text.splitlines()

    calories = int(lines[0].split(":")[1].strip())
    protein = int(lines[1].split(":")[1].strip())
    fat = int(lines[2].split(":")[1].strip())
    carbs = int(lines[3].split(":")[1].strip())
    

    context.user_data["total_calories"] += calories
    context.user_data["total_protein"] += protein
    context.user_data["total_fat"] += fat
    context.user_data["total_carbs"] += carbs
    

    return HAVAL


async def total_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    calories = context.user_data.get("total_calories",0 )
    protein = context.user_data.get("total_protein",0 )
    fat = context.user_data.get("total_fat",0 )
    carbs = context.user_data.get("total_carbs",0 )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
Калории: {calories}
Белки: {protein}
Жиры: {fat}
Углеводы: {carbs}
"""
    )


async def new_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["total_calories"] = 0
    context.user_data["total_protein"] = 0
    context.user_data["total_fat"] = 0
    context.user_data["total_carbs"] = 0
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"новый день! все данные обнулены"
    )
