import logging

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from handlers.knb_handlers import knb, knb_start
from handlers.gadalka_handlers import gadalka, gadalka_star
from config.states import KNB , MAINMENU , TALK , GADAL
from handlers.talk_handlers import talk, talk_start
from dotenv import load_dotenv
import os
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['/start_knb'], ['3']]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет. Напиши /start_knb - чтобы поиграть в камень ножницы бумага , /start_talk - чтобы поговорить или /gadalka_star чтобы погадать ",
        reply_markup=markup
    )
    return MAINMENU



        

if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(os.getenv('TELEGRAM_TOKEN'))
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
            CommandHandler("start_knb", knb_start),
            CommandHandler("start_talk", talk_start),
            CommandHandler("gadalka_star", gadalka_star),
            ],
            KNB: [MessageHandler(filters.TEXT & ~filters.COMMAND, knb)],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            GADAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, gadalka)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling()
