import logging
import os

from dotenv import load_dotenv
from telegram import (
    ReplyKeyboardMarkup,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    PicklePersistence,
    filters,
)

from config.states import GADAL, GET_NORMA, HAVAL, KNB, MAINMENU, TALK, GET_PRODUKS
from handlers.gadalka_handlers import gadalka, gadalka_star
from handlers.haval_handlers import (
    get_norma,
    haval,
    haval_start,
    new_day,
    norma_star,
    total_start,
    yveren_star,
    holod,
    holod_start,
)
from handlers.knb_handlers import knb, knb_start
from handlers.talk_handlers import talk, talk_start
from handlers.start_handler import start

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


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


if __name__ == "__main__":
    persistence = PicklePersistence("cache")

    application = (
        ApplicationBuilder()
        .token(os.getenv("TELEGRAM_TOKEN"))
        .persistence(persistence)
        .build()
    )

    # Handler - обработчик
    # CommandHandler - обработчик команд
    # join - присоединение
    # request - запрос

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("Knb", knb_start),
                CommandHandler("Talk", talk_start),
                CommandHandler("Gadalka", gadalka_star),
                CallbackQueryHandler(knb_start, pattern="^knb$"),
                CallbackQueryHandler(talk_start, pattern="^talk$"),
                CallbackQueryHandler(gadalka_star, pattern="^gadalka$"),
                CallbackQueryHandler(norma_star, pattern="^norma$"),
                CommandHandler("Total", total_start),
                CommandHandler("New_day", new_day),
                CommandHandler("norma", norma_star),
            ],
            GET_NORMA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_norma),
                CallbackQueryHandler(start, pattern="^back_1$"),
            ],
            KNB: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, knb),
                CallbackQueryHandler(start, pattern="^back_2$"),
            ],
            TALK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, talk),
                CallbackQueryHandler(start, pattern="^back$"),
            ],
            GADAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, gadalka),
                CallbackQueryHandler(start, pattern="^back_3$"),
            ],
            HAVAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, haval),
                CommandHandler("Total", total_start),
                CommandHandler("New_day", new_day),
                CommandHandler("holodilnik", holod),
                CallbackQueryHandler(yveren_star, pattern="^new_day$"),
                CallbackQueryHandler(norma_star, pattern="^restart$"),
                CallbackQueryHandler(total_start, pattern="^total$"),
                CallbackQueryHandler(new_day, pattern="^yes$"),
                CallbackQueryHandler(haval, pattern="^no$"),
                CallbackQueryHandler(holod_start, pattern="^holod$"),
                CallbackQueryHandler(haval, pattern="^holod_1$"),
            ],
            GET_PRODUKS:[MessageHandler(filters.TEXT & ~filters.COMMAND, holod),

            ]
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name="main_conversation",
    )
    # Владмиир не молодец
    application.add_handler(conv_handler)

    application.run_polling()
