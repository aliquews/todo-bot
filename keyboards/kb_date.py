from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октбярь", "Ноябрь", "Декабрь"]
def kb_year():
    builder = ReplyKeyboardBuilder()
    for i in range(2022, 2031):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def kb_month():
    builder = ReplyKeyboardBuilder()
    for i in months:
        builder.add(KeyboardButton(text=i))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def kb_day():
    builder = ReplyKeyboardBuilder()
    for i in range(1,32):
        builder.add(KeyboardButton(text=str(i).rjust(2,'0')))
    builder.adjust(7)
    return builder.as_markup(resize_keyboard=True)
