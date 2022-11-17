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
    if len(list(builder.as_markup())[0][1]):
        await message.answer("Твой список задач!\nЕсли ты хочешь завершить задачу - <b>просто нажми на неё</b>",reply_markup=builder.as_markup(), parse_mode="HTML")
    else:
        await message.answer("Нет активных задач.", parse_mode="HTML")
async def del_task(callback: CallbackQuery, callback_data: MyCallbackFactory):

    db.del_task_db(callback.message.chat.id, callback_data.text)

    builder = InlineKeyboardBuilder()
    id = 0
    for txt in db.inline_list(callback.message.chat.id):
        builder.button(
            text = txt,
            callback_data=MyCallbackFactory(action="delete",text=txt)
        )
        id+=1

    builder.adjust(1)
    if callback_data.action == "delete" and len(list(builder.as_markup())[0][1]) != 0:
        await callback.message.edit_text("Твой список задач!\nЕсли ты хочешь завершить задачу - <b>просто нажми на неё</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    else:
        await callback.message.edit_text("Нет активных задач.", parse_mode="HTML")
    await callback.answer("Задача удалена!")


@router.callback_query(MyCallbackFactory.filter())
async def update_task(callback: CallbackQuery, callback_data: MyCallbackFactory):
    if callback_data.action == "delete":
        await del_task(callback, callback_data)
        await callback.answer("Задача удалена!")
