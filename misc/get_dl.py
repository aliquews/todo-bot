from datetime import datetime
from misc.tables import Tasks, User, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

def get_text(chat_id: int) -> str:
    text = list()
    with Session(engine) as session:
        usr_id = select(User.id).where(User.tgid == chat_id)
        stmt = select(Tasks).where(Tasks.user_id == usr_id)
        for task in session.scalars(stmt):
            tmp_text = list()
            tmp_tsk = task.task + ', дедлайн: '
            tmp_text.append(tmp_tsk)
            dl = str(task.deadline).split('-')
            tmp_dl = ''
            days = (datetime(int(dl[0]), int(dl[1]), int(dl[2])) - datetime.today()).days + 1

            if days < 0:
                tmp_dl += '<b>срок окончания прошел</b> ❗️\n'
            elif days == 0:
                tmp_dl += 'срок окончания -<b>сегодня</b>❗️\n'
            elif(days == 1):
                tmp_dl += 'срок окончания -<b>до завтра</b> 🔴\n'

            elif(1 < days < 7 and (days % 10 in (2,3,4))):
                tmp_dl += f'срок окончания -<b>через {days} дня</b> 🟡\n'

            elif(1 < days < 7):
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
