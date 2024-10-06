import asyncio
from aiogram import Dispatcher
from app.handlers import router
from bot_instance import bot  # Импортируйте bot из нового файла

dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
