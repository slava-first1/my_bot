
import random
from telegram import Update 
from telegram.ext import (
    ContextTypes,
    
)
from config.states import GADAL
async def gadalka_star(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="привет, я гадалка, задай любой вопрос",
        
    )
    return GADAL


async def gadalka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text.lower()

    many = [
        "достаточно",
        "много",
        "мало",
        "могло быть и меньше",
        "могло быть и больше",
    ]
    when = [
        "вчера",
        "завтра",
        "никогда",
        "летом",
        "зимой"
    ]
   
    yesno = [
        'да',
        'нет'
    ]
    why = [
        "покачену",
        "потому что",
        "так надо",
        "радуйся тому что есть",
        "больше не пиши сюда"
    ]

    if 'сколько' in text:
        bot_var = random.choice(many)

    elif 'когда' in text:
        bot_var = random.choice(when)

    elif 'почему' in text:
        bot_var = random.choice(why)
      
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{bot_var}"
      )
    

    else:
        bot_var = random.choice(yesno)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{bot_var},"
        )