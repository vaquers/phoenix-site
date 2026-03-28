import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, Chat
from config import router, BOT_TOKEN

import handlers.main_handlers
import handlers.admin_handlers
import handlers.community_channel_handlers
from utils.middleware import AccessControlMiddleware, ThrottledMiddleware


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.message.middleware(AccessControlMiddleware())
    dp.message.middleware(ThrottledMiddleware())
    dp.callback_query.middleware(AccessControlMiddleware())

    dp.include_router(handlers.community_channel_handlers.router)
    dp.include_router(handlers.admin_handlers.router)
    dp.include_router(router)
    
    await bot.set_my_commands([
            BotCommand(command="start", description="🚀 Запустить бота"),
        ])
    # Явно запрашиваем channel_post, иначе бот не получит посты из канала
    await dp.start_polling(
        bot,
        allowed_updates=["message", "callback_query", "channel_post", "edited_channel_post"],
    )

if __name__ == "__main__":
    asyncio.run(main())