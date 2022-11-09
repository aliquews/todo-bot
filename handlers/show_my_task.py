from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters.callback_data import CallbackData
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.tables import User, Tasks, engine


class MyCallbackFactory(CallbackData, prefix="task"):
    action: str
    text: str

router = Router()
@router.message(Text(text="Мои задачи"))
async def show_tasks(message:Message):
    builder = InlineKeyboardBuilder()
    session = Session(engine)
    usrid = session.scalar(select(User.id).where(User.tgid == message.from_user.id))
    stmt = select(Tasks.task).where(Tasks.user_id == usrid)
    id = 0
    for txt in session.scalars(stmt):
        builder.button(
            text = txt,
            callback_data=MyCallbackFactory(action="delete",text=txt)
        )
        id+=1
    builder.adjust(1)
    session.close()
    await message.answer("Твой список задач!\nЕсли ты хочешь завершить задачу - <b>просто нажми на неё</b>",reply_markup=builder.as_markup(), parse_mode="HTML")


async def del_task(message: Message, text: str):
    session = Session(engine)

    usr_id = session.scalar(select(User.id).where(User.tgid == message.chat.id))
    stm = session.get(Tasks, session.scalar(select(Tasks.id).where(Tasks.task == text).where(Tasks.user_id == usr_id)))

    session.delete(stm)
    session.commit()

    builder = InlineKeyboardBuilder()
    stmt = select(Tasks.task).where(Tasks.user_id == usr_id)
    id = 0
    for txt in session.scalars(stmt):
        builder.button(
            text = txt,
            callback_data=MyCallbackFactory(action="delete",text=txt)
        )
        id+=1

    builder.adjust(1)
    session.close()
    await message.edit_text("Твой список задач!\nЕсли ты хочешь завершить задачу - <b>просто нажми на неё</b>", reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(MyCallbackFactory.filter())
async def update_task(callback: CallbackQuery, callback_data: MyCallbackFactory):
    if callback_data.action == "delete":
        await del_task(callback.message, callback_data.text)
    await callback.answer("Задача удалена!")
