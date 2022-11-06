from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters.callback_data import CallbackData
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from misc.tables import Base, User, Tasks, engine
from typing import Optional
from magic_filter import F

class MyCallbackFactory(CallbackData, prefix="task"):
    action: str
    value: Optional[int]


router = Router()


@router.message(Text(text="My tasks"))
async def show_tasks(message:Message):
    builder = InlineKeyboardBuilder()
    session = Session(engine)
    stmt = select(Tasks.task).where(Tasks.user_id == 1)
    id = 0
    for txt in session.scalars(stmt):
        builder.button(
            text = txt,
            callback_data=MyCallbackFactory(action="delete",value=id)
        )
        id+=1
    builder.adjust(1)
    session.close()
    await message.answer("This is yours list of task!\nIf you want to complete the task - <b>just click them</b>",reply_markup=builder.as_markup(), parse_mode="HTML")


async def del_task(message: Message, text: str):
    session = Session(engine)
    usr_id = session.scalar(select(User.id).where(User.tgid == message.from_user.id))
    stmt = session.get(Tasks, session.scalar(select(Tasks.id).where(Tasks.task == text).where(Tasks.user_id == usr_id)))
    session.execute(stmt)
    session.commit()
    builder = InlineKeyboardBuilder()
    stmt = select(Tasks.task).where(Tasks.user_id == 1)
    id = 0
    for txt in session.scalars(stmt):
        builder.button(
            text = txt,
            callback_data=MyCallbackFactory(action="delete",value=id)
        )
        id+=1
    builder.adjust(1)
    session.close()
    await message.edit_text("This is yours list of task!\nIf you want to complete the task - <b>just click them</b>\n(TEST)", reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(MyCallbackFactory.filter())
async def update_task(callback: CallbackQuery, callback_data: MyCallbackFactory):
    if callback_data.action == "delete":
        await del_task(callback.message, callback.message.text)
    await callback.answer()
