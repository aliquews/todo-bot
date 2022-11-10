from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.text import Text
from db.database import db
from callback.MyCallbackFactory import MyCallbackFactory

router = Router()
@router.message(Text(text="Мои задачи"))
async def show_tasks(message:Message):
    builder = InlineKeyboardBuilder()
    id = 0
    for txt in db.inline_list(message.chat.id):
        builder.button(
            text = txt,
            callback_data=MyCallbackFactory(action="delete",text=txt)
        )
        id+=1
    builder.adjust(1)
    await message.answer("Твой список задач!\nЕсли ты хочешь завершить задачу - <b>просто нажми на неё</b>",reply_markup=builder.as_markup(), parse_mode="HTML")


async def del_task(message: Message, text: str):

    db.del_task_db(message.chat.id, text)

    builder = InlineKeyboardBuilder()
    id = 0
    for txt in db.select_task(message.chat.id):
        builder.button(
            text = txt,
            callback_data=MyCallbackFactory(action="delete",text=txt)
        )
        id+=1

    builder.adjust(1)
    await message.edit_text("Твой список задач!\nЕсли ты хочешь завершить задачу - <b>просто нажми на неё</b>", reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(MyCallbackFactory.filter())
async def update_task(callback: CallbackQuery, callback_data: MyCallbackFactory):
    if callback_data.action == "delete":
        await del_task(callback.message, callback_data.text)
    await callback.answer("Задача удалена!")
