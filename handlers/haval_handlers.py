from telegram import (
    Update,
    # ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
from openai import OpenAI
from config.states import HAVAL, GET_NORMA, GET_PRODUKS



async def norma_star(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                "Назад", callback_data="back_1", api_kwargs={"style": "danger"}
            )
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Введите данные о себе в формате:\nм 25 180 75\n(пол возраст рост вес)",
        reply_markup=markup,
    )

    return GET_NORMA


async def haval_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    # success, primary
    keyboard = [
        [
            InlineKeyboardButton(
                "Назад", callback_data="back", api_kwargs={"style": "danger"}
            )
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Введите что вы съели", reply_markup=markup)

    return HAVAL


async def get_norma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    keyboard = (
        [
            InlineKeyboardButton(
                "перепройдти", callback_data="restart", api_kwargs={"style": "success"}
            ),
            InlineKeyboardButton("что я могу приготовить ?", callback_data="holod"),
        ],
    )
    markup = InlineKeyboardMarkup(keyboard)

    text = update.effective_message.text

    sex, age, height, weight = text.split()

    age = int(age)
    height = int(height)
    weight = float(weight)

    if sex.lower() == "м":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    calories = int(bmr * 1.55)

    protein = int(weight * 2)
    fat = int(weight)
    carbs = int((calories - protein * 4 - fat * 9) / 4)

    context.user_data["norma"] = {
        "calories": calories,
        "protein": protein,
        "fat": fat,
        "carbs": carbs,
    }

    context.user_data["total_calories"] = 0
    context.user_data["total_protein"] = 0
    context.user_data["total_fat"] = 0
    context.user_data["total_carbs"] = 0

    await update.effective_message.reply_text(
        f"""Ваша норма:

Калории: {calories}
Белки: {protein}
Жиры: {fat}
Углеводы: {carbs}

Теперь отправляйте что вы съели
""",
        reply_markup=markup,
    )

    return HAVAL


async def holod_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                "Назад", callback_data="back_3", api_kwargs={"style": "danger"}
            )
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "*напиши\!\. что у тебя в холодильнике\:*", reply_markup=markup, parse_mode="MarkdownV2"
    )

    return GET_PRODUKS


async def holod(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.effective_message.text

    client = OpenAI()

    lst = [
        {
            "role": "developer",
            "content": "выдовай пошаговые инструкций возможных блюд изходя от ингредиентов которые написал человек. Форматируй ответы для  parse_mode HTML в telegram боте",
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
        chat_id=update.effective_chat.id,
        text=f"{response.output_text}",
        parse_mode="HTML",
    )


async def haval(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.effective_message.text

    client = OpenAI()

    lst = [
        {
            "role": "developer",
            "content": """ "отвечай сколько КБЖУ моей еде только числами в формате:"
             калорий: N
             белки: N
             жиры: N
             углеводы: N
             """,
        }
    ] + [
        {"role": "user", "content": text},
    ]

    response = client.responses.create(
        model="gpt-5.4-nano",
        reasoning={"effort": "low"},
        input=lst,
    )
    query = update.callback_query
    if query:
        await query.answer()
    keyboard = (
        [
            InlineKeyboardButton("всего вы съели", callback_data="total"),
            InlineKeyboardButton("зброс данных", callback_data="new_day"),
        ],
    )
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{response.output_text} \n что ты еще ел ? ",
        reply_markup=markup,
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

    calories = context.user_data.get("total_calories", 0)
    protein = context.user_data.get("total_protein", 0)
    fat = context.user_data.get("total_fat", 0)
    carbs = context.user_data.get("total_carbs", 0)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"""
Калории: {calories} из {get_norma("calories, 0")}
Белки: {protein} из 
Жиры: {fat} из 
Углеводы: {carbs} из 
""",
    )


async def yveren_star(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                "нет", callback_data="no", api_kwargs={"style": "danger"}
            ),
            InlineKeyboardButton(
                "да", callback_data="yes", api_kwargs={"style": "primary"}
            ),
        ]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("вы уверены", reply_markup=markup)

    return HAVAL


async def new_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()

    context.user_data["total_calories"] = 0
    context.user_data["total_protein"] = 0
    context.user_data["total_fat"] = 0
    context.user_data["total_carbs"] = 0
    await query.edit_message_text("новый день! все данные обнулены")
