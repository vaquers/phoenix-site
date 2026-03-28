from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def cmd_reception(message: Message, state: FSMContext):
    await message.answer("Раздел «Запись» в разработке.")
