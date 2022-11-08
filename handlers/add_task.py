from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from misc.tables import Base, User, Tasks
from keyboards.kb_date import kb_day, kb_month, kb_year, months
from keyboards.main_kb import main_kb


class AddTask(StatesGroup):
    enter_task = State()
    enter_year = State()
    enter_month = State()
    enter_day = State()


engine = create_engine("postgresql+psycopg2://postgres:111@localhost/newdb")

router = Router()

convert = dict(zip(months, [i for i in range(1,13)]))

convert_date = list()

txt = list()

@router.message(Text(text="Добавить задачу"))
async def add_task(message:Message, state: FSMContext):
    await message.answer("Напиши мне задачу")
    await state.set_state(AddTask.enter_task)

@router.message(state=AddTask.enter_task)
async def ent_task(message: Message, state: FSMContext):
    with Session(engine) as session:
        stmt = select(User.id).where(User.tgid == message.from_user.id)
        tsk = Tasks(
            task = message.text,
            user_id = session.scalar(stmt)
        )
        session.add_all([tsk])
        session.commit()
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

    with Session(engine) as session:
        session.execute(
            update(Tasks)
            .where(Tasks.task == txt[0])
            .values(deadline=sqldate)
        )
        session.commit()
    txt.clear()
    await message.answer("Задача успешно создана!", reply_markup=main_kb())
    await state.clear()
