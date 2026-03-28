import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, Chat
from config import router


import handlers.reception_handlers
import handlers.main_handlers
import utils

async def main():
    bot = Bot(token="8357947641:AAFuWLR_F3tJgGp41ZboX8Dy9BFy0B5DL_Y")
    dp = Dispatcher()
    dp.message.middleware(utils.middleware.RegisterMiddleware())
    dp.message.middleware(utils.middleware.ThrottledMiddleware())

    dp.include_router(router)
    
    await bot.set_my_commands([
            BotCommand(command="start", description="🚀 Запустить бота"),
            BotCommand(command="admin", description="🔑 Назначить администратора"),
        ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())