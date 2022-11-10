from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.text import Text
from keyboards.kb_date import kb_day, kb_month, kb_year
from misc.tmpvar import *
from keyboards.main_kb import main_kb
from states.AddTask import AddTask
from db.database import db

router = Router()

@router.message(Text(text="Добавить задачу"))
async def add_task(message:Message, state: FSMContext):
    await message.answer("Напиши мне задачу")
    await state.set_state(AddTask.enter_task)

@router.message(state=AddTask.enter_task)
async def ent_task(message: Message, state: FSMContext):
    db.task_add_to_db(message.text, message.chat.id)
    txt.append(message.text)
    await message.answer("Задача добавлена!")
    await message.answer("Теперь задай дедлайн для задачи\n Год?", reply_markup=kb_year())
    await state.set_state(AddTask.enter_year)


@router.message(state=AddTask.enter_year)
async def ent_year(message: Message, state: FSMContext):
    convert_date.append(message.text)
    await message.answer("Месяц?", reply_markup=kb_month())
    await state.set_state(AddTask.enter_month)


@router.message(state=AddTask.enter_month)
async def ent_month(message: Message, state: FSMContext):
    convert_date.append(str(convert[message.text]))
    await message.answer("Число?", reply_markup=kb_day())
    await state.set_state(state=AddTask.enter_day)


@router.message(state=AddTask.enter_day)
async def ent_month(message: Message, state: FSMContext):
    convert_date.append(message.text)
    sqldate = '-'.join(convert_date)
    convert_date.clear()
    db.add_deadline(txt, sqldate)
    txt.clear()
    await message.answer("Задача успешно создана!", reply_markup=main_kb())
    await state.clear()
