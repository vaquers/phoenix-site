from aiogram.types import Message


async def questions(message: Message, *_):
    await message.answer("Раздел «Вопросы» в разработке.")
