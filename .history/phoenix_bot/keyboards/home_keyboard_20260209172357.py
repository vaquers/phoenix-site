from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def home_keyboard():
    buttons = [
        [
            types.KeyboardButton(text="📖 про нас"),
            types.KeyboardButton(text="👥 команда")
        ],
        [
            types.KeyboardButton(text="📽️ блог"),
            types.KeyboardButton(text=" спонсоры")
        ],
        [
            types.KeyboardButton(text="📧 контакты"),
            types.KeyboardButton(text="🧾 анкеты")
        ]
    ]

    markup = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    return markup


async def home_keyboard_for_admin():
    """
    Клавиатура для is_admin=True без дополнительных пунктов
    «запись / цены / вопросы».
    Сейчас совпадает с обычной домашней клавиатурой.
    """
    return await home_keyboard()