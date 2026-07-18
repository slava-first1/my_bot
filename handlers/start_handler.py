
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)

from config.states import MAINMENU



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "кнб", callback_data="knb", api_kwargs={"style": "primary"}
            )
        ],
        [
            InlineKeyboardButton(
                "разговор с ии", callback_data="talk", api_kwargs={"style": "success"}
            )
        ],
        [
            InlineKeyboardButton(
                "гадалка", callback_data="gadalka", api_kwargs={"style": "primary"}
            )
        ],
        [
            InlineKeyboardButton(
                "вычти свою ному кбжу",
                callback_data="norma",
                api_kwargs={"style": "success"},
            )
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if "total_protein" not in context.user_data:
        context.user_data["total_protein"] = 0

    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            text="Привет. выбери что хочешь поделать!",
            reply_markup=markup,
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Привет. выбери что хочешь поделать!",
            reply_markup=markup,
        )
    return MAINMENU