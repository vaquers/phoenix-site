from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import router
from datetime import datetime
from db.queries.user_queries import get_user
from keyboards.home_keyboard import home_keyboard, home_keyboard_for_admin
from handlers.reception_handlers import cmd_reception
from states.back_states import BackFSM
from handlers.price_handlers import price
from handlers.questions_handlers import questions


def _time_greeting():
    hour = datetime.now().hour
    if 0 <= hour < 4:
        return "Доброй ночи"
    if hour < 12:
        return "Доброе утро"
    if hour < 16:
        return "Добрый день"
    return "Добрый вечер"


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    name = message.from_user.full_name or "Пользователь"
    user_row = get_user(user_id)

    if user_row is None:
        await message.answer("У вас нет доступа к боту.")
        return

    _, is_admin = user_row
    time_text = _time_greeting()
    if is_admin:
        await message.answer(
            f"{time_text}, {name}!",
            reply_markup=await home_keyboard_for_admin(),
        )
    else:
        await message.answer(
            f"{time_text}, {name}!",
            reply_markup=await home_keyboard(),
        )


@router.message(F.text)
async def menu_handler(message: Message, state: FSMContext):
    text = message.text
    if text == "📅 запись":
        await cmd_reception(message, state)
    elif text == "💵 цены":
        await price(message, state)
    elif text == "❔ вопросы":
        await questions(message, state)
    elif text == "↩️":
        current_state = await state.get_state()
        if current_state == BackFSM.first_back:
            await message.answer("Главное меню", reply_markup=await home_keyboard())
