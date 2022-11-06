from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from misc.tables import Base, User, Tasks


class AddTask(StatesGroup):
    enter_task = State()


engine = create_engine("postgresql+psycopg2://postgres:111@localhost/newdb")

router = Router()

@router.message(Text(text="Add new task"))
async def add_task(message:Message, state: FSMContext):
    await message.answer("Please enter your task")
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
    await message.answer("Your task succesfully added!")
    await state.clear()
