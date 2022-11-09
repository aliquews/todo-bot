from aiogram import Router
from aiogram.types import Message
from db.tables import Base, User, Tasks
from sqlalchemy import create_engine, select, exists
from sqlalchemy.orm import Session
from keyboards.main_kb import main_kb

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
    await message.answer("Привет! Я бот для задач =)", reply_markup=main_kb())
