from datetime import datetime
from db.database import db

def get_text(chat_id: int) -> str:
    text = list()
    data = db.tasks_dl(chat_id)
    for i in data.keys():
        tmp_text = list()
        tmp_text.append(i +', <b><i>дедлайн:</i></b> ')
        tmp_dl = ''
        days = (datetime(int(data[i][0]), int(data[i][1]), int(data[i][2])) - datetime.today()).days + 1

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
