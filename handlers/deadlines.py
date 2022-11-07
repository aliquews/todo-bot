from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters.text import Text
from misc.tables import Tasks, User, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

router = Router()

def get_text(message: Message):
    session = Session(engine)
    stmt = select(Tasks)
    session.close()

@router.message(Text(text="Дедлайны"))
async def show_deadlines(message: Message):
    pass
