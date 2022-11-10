import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import start, add_task, show_my_task, deadlines, notifications
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(API_TOKEN)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()

    dp.include_router(start.router)
    dp.include_router(add_task.router)
    dp.include_router(show_my_task.router)
    dp.include_router(deadlines.router)

    scheduler.add_job(notifications.send_message,"cron",hour=9,minute=30, args=(bot,))
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
