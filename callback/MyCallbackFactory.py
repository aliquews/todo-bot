from aiogram.dispatcher.filters.callback_data import CallbackData

class MyCallbackFactory(CallbackData, prefix="task"):
    action: str
    text: str
