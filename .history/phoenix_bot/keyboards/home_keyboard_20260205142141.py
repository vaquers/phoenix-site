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
            types.KeyboardButton(text="🏆 достижения"),
            types.KeyboardButton(text="📖 про нас"),

        ],
        [
            types.KeyboardButton(text="📧 контакты")
            types.KeyboardButton(text="📽️ влог")
        ],
    ]

    markup = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    return markup


async def home_keyboard_for_admin():
    buttons = [
        [
            types.KeyboardButton(text="📅 запись"),
            types.KeyboardButton(text="💵 цены")
        ],
        [
            types.KeyboardButton(text="❔ вопросы"),
            types.KeyboardButton(text="🗣️ отзывы"),
            types.KeyboardButton(text="🎁 сертификаты")
        ],
        [
            types.KeyboardButton(text="👤 пользователи"),
            types.KeyboardButton(text="📊 статистика")
        ]
    ]

    markup = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    return markup