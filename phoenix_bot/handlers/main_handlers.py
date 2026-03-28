from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import router, SUPER_ADMIN_ID
from db.queries.user_queries import get_user
from db.queries.about_queries import get_about_page
from db.queries.team_queries import get_team_page_description
from db.queries.blog_queries import get_blog_page_description
from db.queries.sponsor_queries import get_sponsors_page_description
from db.queries.contact_queries import get_contacts_page
from keyboards.home_keyboard import home_keyboard


def _time_greeting() -> str:
    hour = datetime.now().hour
    if 0 <= hour < 4:
        return "Доброй ночи"
    if hour < 12:
        return "Доброе утро"
    if hour < 16:
        return "Добрый день"
    return "Добрый вечер"


@router.message(CommandStart())
async def start(message: Message) -> None:
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
            f"{time_text}, {name}!\n\n"
            "Вы админ. Используйте команды:\n"
            "/add_user — добавить пользователя\n"
            "/set_admin — выдать или снять права админа",
        )
    else:
        await message.answer(f"{time_text}, {name}!", reply_markup=await home_keyboard())


@router.message(F.text == "📖 про нас")
async def show_about(message: Message) -> None:
    """Показать блок «Про нас» по кнопке."""
    row = get_about_page()
    if row is None:
        await message.answer("Данные «Про нас» ещё не заданы.")
        return

    description, years, team_size = row
    text = (
        "📄 <b>Про нас</b>\n\n"
        f"{description or '(пока пусто)'}\n\n"
        f"🏆 Года в соревнованиях: <b>{years}</b>\n"
        f"👥 Человек в команде: <b>{team_size}</b>"
    )

    # Если супер-админ — показываем кнопки редактирования (inline)
    if message.from_user and message.from_user.id == SUPER_ADMIN_ID:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✏️ Описание", callback_data="about_edit_description"),
                    InlineKeyboardButton(text="✏️ Годы", callback_data="about_edit_years"),
                ],
                [
                    InlineKeyboardButton(text="✏️ Кол-во людей", callback_data="about_edit_team"),
                ],
            ]
        )
        await message.answer(text, parse_mode="HTML", reply_markup=keyboard)
    else:
        await message.answer(text, parse_mode="HTML")


@router.message(F.text == "👥 команда")
async def show_team(message: Message) -> None:
    """Показать описание страницы «Команда» и inline-меню."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    description = get_team_page_description()
    text = f"👥 <b>Команда</b>\n\n{description or '(Описание пока не задано.)'}"

    is_super_admin = message.from_user and message.from_user.id == SUPER_ADMIN_ID
    if is_super_admin:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✏️ Описание страницы", callback_data="team_edit_page_description")],
                [InlineKeyboardButton(text="➕ Добавить члена команды", callback_data="team_add")],
                [InlineKeyboardButton(text="📋 Все члены команды", callback_data="team_list")],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📋 Все члены команды", callback_data="team_list")],
            ]
        )
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.message(F.text == "📽️ блог")
async def show_blog(message: Message) -> None:
    """Показать описание страницы «Блог» и inline‑меню."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    description = get_blog_page_description()
    text = f"📽️ <b>Блог</b>\n\n{description or '(Описание пока не задано.)'}"

    is_super_admin = message.from_user and message.from_user.id == SUPER_ADMIN_ID
    if is_super_admin:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✏️ Описание страницы", callback_data="blog_edit_page_description")],
                [InlineKeyboardButton(text="➕ Добавить запись", callback_data="blog_add")],
                [InlineKeyboardButton(text="📋 Все записи", callback_data="blog_list")],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📋 Все записи", callback_data="blog_list")],
            ]
        )
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.message(F.text == "💰 спонсоры")
async def show_sponsors(message: Message) -> None:
    """Показать описание страницы «Спонсоры» и inline‑меню."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    description = get_sponsors_page_description()
    text = f"💰 <b>Спонсоры</b>\n\n{description or '(Описание пока не задано.)'}"

    is_super_admin = message.from_user and message.from_user.id == SUPER_ADMIN_ID
    if is_super_admin:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✏️ Описание страницы", callback_data="sponsors_edit_page_description")],
                [InlineKeyboardButton(text="➕ Добавить спонсора", callback_data="sponsor_add")],
                [InlineKeyboardButton(text="📋 Все спонсоры", callback_data="sponsor_list")],
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📋 Все спонсоры", callback_data="sponsor_list")],
            ]
        )
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.message(F.text == "📧 контакты")
async def show_contacts(message: Message) -> None:
    """Показать страницу контактов: описание, почта, телефон, адрес, телеграм + инлайн для редактирования и просмотра сообщений."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    row = get_contacts_page()
    if row is None:
        await message.answer("Данные контактов ещё не заданы.")
        return

    description, email, phone, address, telegram = row
    text = (
        "📧 <b>Контакты</b>\n\n"
        f"{description or '(описание не задано)'}\n\n"
        f"📩 <b>Почта:</b> {email or '—'}\n"
        f"📞 <b>Телефон:</b> {phone or '—'}\n"
        f"✈️ <b>Telegram:</b> {telegram or '—'}\n"
        f"📍 <b>Адрес:</b> {address or '—'}"
    )

    is_super_admin = message.from_user and message.from_user.id == SUPER_ADMIN_ID
    if is_super_admin:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✏️ Описание", callback_data="contacts_edit_description")],
                [
                    InlineKeyboardButton(text="✏️ Почта", callback_data="contacts_edit_email"),
                    InlineKeyboardButton(text="✏️ Телефон", callback_data="contacts_edit_phone"),
                ],
                [
                    InlineKeyboardButton(text="✏️ Telegram", callback_data="contacts_edit_telegram"),
                    InlineKeyboardButton(text="✏️ Адрес", callback_data="contacts_edit_address"),
                ],
                [InlineKeyboardButton(text="📋 Все сообщения", callback_data="contacts_messages")],
            ]
        )
    else:
        keyboard = None
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)


@router.message(F.text == "🧾 анкеты")
async def show_join_applications(message: Message) -> None:
    """Показать анкеты с сайта «Стать участником» (только для супер-админа)."""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    if message.from_user and message.from_user.id != SUPER_ADMIN_ID:
        await message.answer("Доступ только для администратора.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Список анкет", callback_data="join_list")],
            [InlineKeyboardButton(text="✏️ Описание страницы", callback_data="join_edit_page_description")],
        ]
    )
    await message.answer(
        "🧾 <b>Анкеты</b>\n\nЗаявки со страницы «Стать участником» на сайте.",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
