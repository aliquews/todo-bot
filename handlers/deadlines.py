from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters.text import Text
from misc.get_dl import get_text

router = Router()


@router.message(Text(text="Дедлайны"))
async def show_deadlines(message: Message):
    await message.answer("Информация по дедлайнам:")
    try:
        await message.answer(get_text(message.chat.id),parse_mode="HTML")
    except:
        await message.answer("Ой-ой, твой список задач пуст")
