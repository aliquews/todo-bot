from aiogram import Bot
from misc.get_dl import get_text
from db.database import db

async def send_message(bot: Bot):
    for user in db.distr():
        try:
            await bot.send_message(text=f"Напоминаю про твои дедлайны🕑\n\n\n{get_text(user)}", chat_id=user, parse_mode="HTML")
        except:
            pass
