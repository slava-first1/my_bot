import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    PicklePersistence,
)

from handlers.knb_handlers import knb, knb_start
from handlers.gadalka_handlers import gadalka, gadalka_star
from handlers.haval_handlers import haval, haval_start, total_start, new_day
from config.states import KNB, MAINMENU, TALK, GADAL, HAVAL
from handlers.talk_handlers import talk, talk_start
from dotenv import load_dotenv
import os


load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["/start_knb"], ["3"]]
    markup = ReplyKeyboardMarkup(keyboard)
    if "total_protein" not in context.user_data:
        context.user_data["total_protein"] = 0
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет. Напиши /Knb - чтобы поиграть в камень ножницы бумага , /Talk - чтобы поговорить или /Gadalka чтобы погадать и еще /Haval и еще /Total , /New_day ",
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
                CommandHandler("Haval", haval_start),
                CommandHandler("Total", total_start),
                CommandHandler("New_day", new_day),
            ],
            KNB: [MessageHandler(filters.TEXT & ~filters.COMMAND, knb)],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            GADAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, gadalka)],
            HAVAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, haval),
                CommandHandler("Total", total_start),
                CommandHandler("New_day", new_day),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name="main_conversation",
    )

    application.add_handler(conv_handler)

    application.run_polling()
