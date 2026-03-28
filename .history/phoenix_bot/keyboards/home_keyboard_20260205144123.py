from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def home_keyboard():
    buttons = [
        [
            types.KeyboardButton(text="👥 команда"),
            types.KeyboardButton(text="📽️ блог")
        ],
        [
            types.KeyboardButton(text="📖 про нас"),
            types.KeyboardButton(text="🧾 анкеты")
        ],
        [
            types.KeyboardButton(text="📧 контакты"),
            types.KeyboardButton(text="📽️ спонсоры")
        ],
        [
            types.KeyboardButton(text="👥 сообщество")
        ]
    ]

    markup = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    return markup