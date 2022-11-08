from aiogram import Bot
from misc.get_dl import get_text
from misc.tables import User, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

async def send_message(bot: Bot):
    with Session(engine) as session:
        usr_id = select(User.tgid)
        for user in session.scalars(usr_id):
            try:
                await bot.send_message(text=f"Напоминаю про твои дедлайны🕑\n\n\n{get_text(user)}", chat_id=user, parse_mode="HTML")
            except:
                pass
