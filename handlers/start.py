from aiogram import Router
from aiogram.types import Message
from keyboards.main_kb import main_kb
from db.database import db

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: Message):
    db.user_add_to_db(message.from_user.id)
    await message.answer("Привет! Я бот для задач =)", reply_markup=main_kb())
