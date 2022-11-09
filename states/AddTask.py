from aiogram.dispatcher.filters.state import State, StatesGroup

class AddTask(StatesGroup):
    enter_task = State()
    enter_year = State()
    enter_month = State()
    enter_day = State()
