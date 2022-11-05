from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from misc.tables import Base, User, Tasks
from sqlalchemy import create_engine, select, exists
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://postgres:111@localhost/newdb")

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: Message):
    session = Session(engine)
    if session.query(exists().where(User.tgid == message.from_user.id)).scalar() == False:
        user = User(
            tgid = message.from_user.id
        )
        session.add_all([user])
        session.commit()
    session.close()
    buttons = [
        [
            KeyboardButton(text="Add new task"),
            KeyboardButton(text="My tasks"),
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    await message.answer("Hello! I'm To do task bot =)", reply_markup=keyboard)
