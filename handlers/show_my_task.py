from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from misc.tables import Base, User, Tasks


router = Router()
@router.message(Text(text="My tasks"))
async def show_tasks(message:Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text = "hello",
        callback_data="test")
    )
    await message.answer("This is test button!",reply_markup=builder.as_markup())
