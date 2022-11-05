import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import start, add_task, show_my_task

logging.basicConfig(level=logging.INFO)

bot = Bot("5745503928:AAG_fWw5wWbDv-HubYxAvOTyR-b_bC-gAdU")
dp = Dispatcher()

async def main():

    dp.include_router(start.router)
    dp.include_router(add_task.router)
    dp.include_router(show_my_task.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
