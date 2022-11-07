from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="Добавить задачу"),
            KeyboardButton(text="Мои задачи"),
        ],

        [
            KeyboardButton(text="Дедлайны"),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
