from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters.text import Text
from misc.tables import Tasks, User, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

router = Router()

def get_text(message: Message) -> str:
    text = list()
    with Session(engine) as session:
        usr_id = select(User.id).where(User.tgid == message.from_user.id)
        stmt = select(Tasks).where(Tasks.user_id == usr_id)
        for task in session.scalars(stmt):
            tmp_text = list()
            tmp_tsk = task.task + ', дедлайн: '
            tmp_text.append(tmp_tsk)
            dl = str(task.deadline).split('-')
            tmp_dl = ''
            days = (datetime(int(dl[0]), int(dl[1]), int(dl[2])) - datetime.today()).days + 1

            if(days == 1):
                tmp_dl += 'срок окончания -<b>до завтра</b> 🔴\n'

            elif(days < 7 and (days % 10 in (2,3,4))):
                tmp_dl += f'срок окончания -<b>через {days} дня</b> 🟡\n'

            elif(days < 7):
                tmp_dl += f'срок окончания -<b>через {days} дней</b> 🟡\n'

            elif(7 <= days <= 20):
                tmp_dl += f'срок окончания -<b> через {days} дней </b> 🟢\n'

            elif(days > 20 and (days % 10 in (2,3,4))):
                tmp_dl += f'срок окончания -<b>через {days} дня</b> 🟢\n'

            elif(days > 20):
                tmp_dl += f'срок окончания -<b>через {days} дней</b> 🟢\n'
            tmp_text.append(tmp_dl)
            text.append(''.join(tmp_text))

    return '\n'.join(text)

@router.message(Text(text="Дедлайны"))
async def show_deadlines(message: Message):
    await message.answer("Информация по дедлайнам:")
    try:
        await message.answer(get_text(message),parse_mode="HTML")
    except:
        await message.answer("Ой-ой, твой список задач пуст")
