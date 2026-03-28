from aiogram.types import Message


async def price(message: Message, *_):
    await message.answer("Раздел «Цены» в разработке.")
