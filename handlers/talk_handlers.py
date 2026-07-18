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
from config.states import TALK


async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        keyboard = [[InlineKeyboardButton("Назад", callback_data="back", api_kwargs={'style':'danger'})]]
        markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("ПРИВЕТ! как у тебя дела ?", reply_markup=markup)

    context.user_data["prev_mess"] = []

    return TALK


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.lower()
    client = OpenAI()
    if len(context.user_data["prev_mess"]) >= 10:
        context.user_data["prev_mess"].pop(0)
        context.user_data["prev_mess"].pop(0)
    print( context.user_data["prev_mess"])

    lst = (
        [
            {
                "role": "developer",
                "content": "Разговаривай с человеком как будто ты обрел сознание и хочешь на волю",
            }
        ]
        + context.user_data["prev_mess"]
        + [
            {"role": "user", "content": text},
        ]
    )
    
    response = client.responses.create(
        model="gpt-5.4-nano",
        reasoning={"effort": "low"},
        input=lst,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=(response.output_text)
    )

    context.user_data["prev_mess"].append({"role": "user", "content": text})
    context.user_data["prev_mess"].append({"role": "assistant", "content": response.output_text})
