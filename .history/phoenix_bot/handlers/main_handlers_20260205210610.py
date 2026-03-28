from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from config import router, hello_text
from datetime import datetime
from db.queries.user_queries import fetch_all_users, add_user, fetch_user_data, make_user_admin, does_an_admin_exist
from keyboards.home_keyboard import home_keyboard, home_keyboard_for_admin
from handlers.reception_handlers import cmd_reception
from states.back_states import BackFSM
from handlers.price_handlers import price
from handlers.questions_handlers import questions


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    name = message.from_user.full_name
    all_users = fetch_all_users()
    all_users = all_users[0] if all_users else []
    time_now = datetime.now().hour
    if time_now >= 0 and time_now < 4:
        time_text = "Доброй ночи"
    elif time_now >= 4 and time_now < 12:
        time_text = "Доброе утро"
    elif time_now >= 12 and time_now < 16:
        time_text = "Добрый день"
    elif time_now >= 16 and time_now < 24:
        time_text = "Добрый вечер"
    if user_id not in all_users and:
        await add_user(user_id, message)
    is_admin = fetch_user_data(user_id)[1]
    if is_admin:
        await message.answer(f"{time_text}, {name}", reply_markup=await home_keyboard())
    else:
        await message.answer(f"Извините, ботом могут пользоваться только администраторы.")


@router.message(Command("admin"))
async def admin(message: Message):
    user_id = message.from_user.id
    does_admin_exist = does_an_admin_exist()
    if does_admin_exist is None:
        await message.answer("Ошибка при проверке наличия администратора")
        return
    admin_status = fetch_user_data(user_id)[1]
    if does_admin_exist:
        if admin_status:
            await message.answer("Вы уже являетесь админом", reply_markup=await home_keyboard_for_admin())
        else:
            await message.answer("У вас нет прав на выполнение этой команды")
    else:
        make_user_admin(user_id)
        if make_user_admin(user_id) is None:
            await message.answer("Ошибка при назначении администратора")
            return
        await message.answer(f"{message.from_user.full_name}, теперь Вы являетесь админом", reply_markup=await home_keyboard_for_admin())


ALTER TABLE users
    RENAME COLUMN junior_admins TO user_id;
@router.message(F.text)
async def menu_handler(message: Message, state: FSMContext):
    text = message.text
    if text == "📅 запись":
        await cmd_reception(message, state)

    elif text == "💵 цены":
        await price(message, state)

    elif text == "❔ вопросы":
        await questions(message, state)

    # elif text == "🗣️ отзывы":
    #     await message.answer(f"отзывы", reply_markup=await review_keyboard())
    #     await state.set_state(BackFSM.first_back)

    # elif text == "🎁 сертификаты":
    #     await message.answer(f"сертификаты", reply_markup=await certificate_keyboard())
    #     await state.set_state(BackFSM.first_back)

    # elif text == "👤 пользователи":
    #     await message.answer(f"пользователи", reply_markup=await user_keyboard())
    #     await state.set_state(BackFSM.first_back)

    # elif text == "📊 статистика":
    #     await message.answer(f"статистика", reply_markup=await statistics_keyboard())
    #     await state.set_state(BackFSM.first_back)

    elif text == "↩️":
        current_state = await state.get_state()
        if current_state == BackFSM.first_back:
            await message.answer("главное меню", reply_markup=await home_keyboard())

