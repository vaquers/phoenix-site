"""
Команды управления доступом и контентом: только супер-админ.
/add_user, /set_admin — доступ.
«📖 про нас» и «👥 команда» — inline‑кнопки, редактирование для супер-админа.
"""
import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import SUPER_ADMIN_ID, COMMUNITY_CHANNEL_USERNAME
from utils.filters import SuperAdminFilter, SuperAdminCallbackFilter
from db.queries.user_queries import add_user, set_admin, user_exists
from db.queries.community_channel_queries import add_channel_post, trim_channel_posts
from db.queries.about_queries import get_about_page, update_about_page
from db.queries.team_queries import (
    get_all_team_members,
    get_team_member,
    add_team_member,
    update_team_member,
    delete_team_member,
    update_team_page_description,
)
from db.queries.blog_queries import (
    get_blog_page_description,
    update_blog_page_description,
    get_all_blog_posts,
    get_blog_post,
    add_blog_post,
    update_blog_post,
)
from db.queries.sponsor_queries import (
    get_sponsors_page_description,
    update_sponsors_page_description,
    get_all_sponsors,
    get_sponsor,
    add_sponsor,
    update_sponsor,
)
from db.queries.contact_queries import (
    get_contacts_page,
    update_contacts_page,
    get_all_contact_messages,
)
from db.queries.join_queries import (
    get_all_join_applications,
    delete_join_application,
    update_join_page_description,
)
from states.about_states import EditAboutFSM
from states.team_states import AddTeamMemberFSM, EditTeamMemberFSM, EditTeamPageDescriptionFSM
from states.blog_states import EditBlogPageDescriptionFSM, AddBlogPostFSM, EditBlogPostFSM
from states.sponsor_states import EditSponsorsPageDescriptionFSM, AddSponsorFSM, EditSponsorFSM
from states.contact_states import EditContactsPageFSM
from states.join_states import EditJoinPageDescriptionFSM

router = Router(name="admin")


@router.message(Command("add_user"), SuperAdminFilter())
async def cmd_add_user(message: Message):
    """
    Формат: /add_user 123 456 789
    Добавляет пользователей с is_admin=False. Если уже есть — пропускает (ON CONFLICT DO NOTHING).
    """
    text = (message.text or "").strip()
    parts = text.split()
    if len(parts) < 2:
        await message.answer(
            "Формат: /add_user <user_id> [user_id ...]\n"
            "Пример: /add_user 123456789 987654321"
        )
        return

    ids_str = parts[1:]
    added = []
    invalid = []
    for s in ids_str:
        if not re.match(r"^-?\d+$", s):
            invalid.append(s)
            continue
        uid = int(s)
        add_user(uid, is_admin=False)
        added.append(uid)

    if invalid:
        await message.answer(f"Не добавлены (не число): {', '.join(invalid)}")
    if added:
        await message.answer(f"Добавлены пользователи: {', '.join(map(str, added))}.")


@router.message(Command("add_community_post"), SuperAdminFilter())
async def cmd_add_community_post(message: Message):
    """
    Добавить посты канала в БД по ID (для отображения на сайте).
    Формат: /add_community_post 120 121 122
    ID берутся из ссылок t.me/phoenixlbsu/120 и т.д.
    """
    text = (message.text or "").strip()
    parts = text.split()
    if len(parts) < 2:
        await message.answer(
            "Формат: /add_community_post <message_id> [message_id ...]\n"
            "Пример: /add_community_post 120 121 122\n"
            "ID можно взять из ссылки на пост: t.me/phoenixlbsu/120 → 120"
        )
        return
    channel = COMMUNITY_CHANNEL_USERNAME.strip().lower()
    added = []
    for s in parts[1:]:
        if not s.isdigit():
            continue
        msg_id = int(s)
        link = f"https://t.me/{COMMUNITY_CHANNEL_USERNAME}/{msg_id}"
        if add_channel_post(channel, msg_id, link, "Пост"):
            added.append(msg_id)
    trim_channel_posts(channel, keep=15)
    if added:
        await message.answer(f"Добавлены посты канала: {', '.join(map(str, added))}. На сайте отобразятся до 3 последних.")
    else:
        await message.answer("Укажите один или несколько числовых ID постов (например: 120 121 122).")


@router.message(Command("set_admin"), SuperAdminFilter())
async def cmd_set_admin(message: Message):
    """
    Формат: /set_admin <user_id> <0|1>
    0 — снять права админа, 1 — назначить админом. Пользователь должен уже быть в таблице.
    """
    text = (message.text or "").strip()
    parts = text.split()
    if len(parts) != 3:
        await message.answer(
            "Формат: /set_admin <user_id> <0|1>\n"
            "Пример: /set_admin 123456789 1"
        )
        return

    try:
        user_id = int(parts[1])
        flag = parts[2]
        if flag not in ("0", "1"):
            await message.answer("Третий аргумент должен быть 0 или 1.")
            return
        is_admin = flag == "1"
    except ValueError:
        await message.answer("user_id должен быть числом.")
        return

    if not user_exists(user_id):
        await message.answer(f"Пользователь {user_id} не найден в таблице. Сначала добавьте его через /add_user.")
        return

    set_admin(user_id, is_admin)
    status = "назначен админом" if is_admin else "снят с прав админа"
    await message.answer(f"Пользователь {user_id} {status}.")


# ---------- Блок «Про нас» (редактирование по inline‑кнопкам) ----------


@router.callback_query(SuperAdminCallbackFilter(), F.data == "about_edit_description")
async def cb_edit_about_description(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditAboutFSM.description)
    await callback.message.answer("Введите новый текст описания блока «Про нас» (одним сообщением):")
    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data == "about_edit_years")
async def cb_edit_about_years(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditAboutFSM.years_in_competitions)
    await callback.message.answer("Введите количество лет в соревнованиях (целое число):")
    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data == "about_edit_team")
async def cb_edit_about_team(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditAboutFSM.team_size)
    await callback.message.answer("Введите количество человек в команде (целое число):")
    await callback.answer()


@router.message(EditAboutFSM.description, F.text)
async def edit_about_description(message: Message, state: FSMContext) -> None:
    new_description = message.text or ""
    row = get_about_page()
    if row is None:
        years, team_size = 0, 0
    else:
        _, years, team_size = row
    update_about_page(new_description, years, team_size)
    await state.clear()
    await message.answer("Описание «Про нас» обновлено.")


@router.message(EditAboutFSM.years_in_competitions, F.text)
async def edit_about_years(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer("Введите одно целое число (например 2).")
        return
    new_years = int(text)
    row = get_about_page()
    if row is None:
        description, team_size = "", 0
    else:
        description, _, team_size = row
    update_about_page(description, new_years, team_size)
    await state.clear()
    await message.answer("Количество лет в соревнованиях обновлено.")


@router.message(EditAboutFSM.team_size, F.text)
async def edit_about_team_size(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text.isdigit():
        await message.answer("Введите одно целое число (например 10).")
        return
    new_team_size = int(text)
    row = get_about_page()
    if row is None:
        description, years = "", 0
    else:
        description, years, _ = row
    update_about_page(description, years, new_team_size)
    await state.clear()
    await message.answer("Количество людей в команде обновлено.")


# ---------- Команда: описание страницы, добавление, список, редактирование ----------


@router.callback_query(SuperAdminCallbackFilter(), F.data == "team_edit_page_description")
async def cb_team_edit_page_description(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditTeamPageDescriptionFSM.description)
    await callback.message.answer("Введите новый текст описания страницы «Команда» (одним сообщением):")
    await callback.answer()


@router.message(EditTeamPageDescriptionFSM.description, F.text)
async def team_page_description_save(message: Message, state: FSMContext) -> None:
    update_team_page_description(message.text or "")
    await state.clear()
    await message.answer("Описание страницы «Команда» обновлено.")


@router.callback_query(SuperAdminCallbackFilter(), F.data == "team_add")
async def cb_team_add(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AddTeamMemberFSM.name)
    await callback.message.answer("Введите имя нового члена команды:")
    await callback.answer()


@router.message(AddTeamMemberFSM.name, F.text)
async def team_add_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=(message.text or "").strip())
    await state.set_state(AddTeamMemberFSM.photo)
    await message.answer("Отправьте фото (или текст «пропустить» без фото):")


@router.message(AddTeamMemberFSM.photo, F.photo)
async def team_add_photo_photo(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await state.set_state(AddTeamMemberFSM.specialty)
    await message.answer("Введите специальность (например: Инженер-моделлер):")


@router.message(AddTeamMemberFSM.photo, F.text)
async def team_add_photo_skip(message: Message, state: FSMContext) -> None:
    if (message.text or "").strip().lower() in ("пропустить", "пропустить без фото", "-"):
        await state.update_data(photo="")
    await state.set_state(AddTeamMemberFSM.specialty)
    await message.answer("Введите специальность (например: Инженер-моделлер):")


@router.message(AddTeamMemberFSM.specialty, F.text)
async def team_add_specialty(message: Message, state: FSMContext) -> None:
    await state.update_data(specialty=(message.text or "").strip())
    await state.set_state(AddTeamMemberFSM.status)
    await message.answer("Введите статус (или «пропустить»):")


@router.message(AddTeamMemberFSM.status, F.text)
async def team_add_status(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if text.lower() in ("пропустить", "-"):
        text = ""
    await state.update_data(status=text)
    await state.set_state(AddTeamMemberFSM.description)
    await message.answer("Введите описание (или «пропустить»):")


@router.message(AddTeamMemberFSM.description, F.text)
async def team_add_description(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if text.lower() in ("пропустить", "-"):
        text = ""
    data = await state.get_data()
    name = data.get("name", "")
    specialty = data.get("specialty", "")
    status = data.get("status", "")
    photo = data.get("photo", "")
    mid = add_team_member(name, specialty, text, status, photo)
    await state.clear()
    if mid is not None:
        await message.answer(f"Член команды «{name}» добавлен (id={mid}).")
    else:
        await message.answer("Ошибка при добавлении.")


@router.callback_query(F.data == "team_list")
async def cb_team_list(callback: CallbackQuery) -> None:
    """Показать всех членов команды: фото, имя, специальность, статус, описание + кнопки редактирования для супер-админа."""
    members = get_all_team_members()
    if not members:
        await callback.message.answer("Пока ни одного члена команды.")
        await callback.answer()
        return

    is_super_admin = callback.from_user and callback.from_user.id == SUPER_ADMIN_ID

    for mid, name, specialty, description, status, photo in members:
        caption = (
            f"<b>{name}</b>\n"
            f"Специальность: {specialty or '—'}\n"
            f"Статус: {status or '—'}\n"
            f"Описание: {description or '—'}"
        )
        if is_super_admin:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="✏️ Имя", callback_data=f"team_edit_{mid}_name"),
                        InlineKeyboardButton(text="✏️ Фото", callback_data=f"team_edit_{mid}_photo"),
                    ],
                    [
                        InlineKeyboardButton(text="✏️ Специальность", callback_data=f"team_edit_{mid}_specialty"),
                        InlineKeyboardButton(text="✏️ Статус", callback_data=f"team_edit_{mid}_status"),
                    ],
                    [InlineKeyboardButton(text="✏️ Описание", callback_data=f"team_edit_{mid}_description")],
                    [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"team_delete_{mid}")],
                ]
            )
        else:
            keyboard = None

        if photo:
            try:
                await callback.message.answer_photo(photo=photo, caption=caption, parse_mode="HTML", reply_markup=keyboard)
            except Exception:
                await callback.message.answer(caption, parse_mode="HTML", reply_markup=keyboard)
        else:
            await callback.message.answer(caption, parse_mode="HTML", reply_markup=keyboard)

    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data.startswith("team_edit_"))
async def cb_team_edit(callback: CallbackQuery, state: FSMContext) -> None:
    """Начать редактирование поля члена команды. callback_data = team_edit_<id>_<field>."""
    parts = callback.data.split("_")
    if len(parts) != 4:
        await callback.answer()
        return
    _, _, mid_str, field = parts
    try:
        member_id = int(mid_str)
    except ValueError:
        await callback.answer()
        return
    if field not in ("name", "photo", "specialty", "status", "description"):
        await callback.answer()
        return
    member = get_team_member(member_id)
    if not member:
        await callback.answer("Член команды не найден.")
        return
    await state.update_data(team_edit_member_id=member_id, team_edit_field=field)
    await state.set_state(EditTeamMemberFSM.value)
    prompts = {
        "name": "Введите новое имя:",
        "photo": "Отправьте новое фото (или текст «пропустить»):",
        "specialty": "Введите новую специальность:",
        "status": "Введите новый статус (или «пропустить»):",
        "description": "Введите новое описание (или «пропустить»):",
    }
    await callback.message.answer(prompts[field])
    await callback.answer()


@router.message(EditTeamMemberFSM.value, F.photo)
async def team_edit_value_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    mid = data.get("team_edit_member_id")
    field = data.get("team_edit_field")
    if field != "photo" or mid is None:
        await state.clear()
        return
    file_id = message.photo[-1].file_id
    member = get_team_member(mid)
    if not member:
        await state.clear()
        await message.answer("Член команды не найден.")
        return
    _, name, specialty, description, status, _ = member
    update_team_member(mid, name, specialty, description, status, file_id)
    await state.clear()
    await message.answer("Фото обновлено.")


@router.message(EditTeamMemberFSM.value, F.text)
async def team_edit_value_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    mid = data.get("team_edit_member_id")
    field = data.get("team_edit_field")
    if mid is None or field is None:
        await state.clear()
        return
    member = get_team_member(mid)
    if not member:
        await state.clear()
        await message.answer("Член команды не найден.")
        return
    _, name, specialty, description, status, photo = member
    value = (message.text or "").strip()
    if value.lower() in ("пропустить", "-"):
        value = ""
    if field == "name":
        name = value
    elif field == "photo":
        photo = value
    elif field == "specialty":
        specialty = value
    elif field == "status":
        status = value
    elif field == "description":
        description = value
    update_team_member(mid, name, specialty, description, status, photo)
    await state.clear()
    await message.answer("Готово.")


# ---------- Удаление члена команды (с подтверждением) ----------


@router.callback_query(SuperAdminCallbackFilter(), F.data.startswith("team_delete_"))
async def cb_team_delete_ask(callback: CallbackQuery) -> None:
    """Спросить подтверждение удаления. callback_data = team_delete_<id>."""
    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.answer()
        return
    try:
        member_id = int(parts[2])
    except ValueError:
        await callback.answer()
        return
    member = get_team_member(member_id)
    if not member:
        await callback.answer("Член команды не найден.")
        return
    name = member[1]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да, удалить", callback_data=f"team_confirm_delete_{member_id}"),
                InlineKeyboardButton(text="Отмена", callback_data="team_cancel_delete"),
            ],
        ]
    )
    await callback.message.answer(
        f"Удалить <b>{name}</b> из команды?",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data.startswith("team_confirm_delete_"))
async def cb_team_confirm_delete(callback: CallbackQuery) -> None:
    """Подтверждение удаления. callback_data = team_confirm_delete_<id>."""
    parts = callback.data.split("_")
    if len(parts) != 4:
        await callback.answer()
        return
    try:
        member_id = int(parts[3])
    except ValueError:
        await callback.answer()
        return
    delete_team_member(member_id)
    await callback.answer("Член команды удалён.")
    try:
        await callback.message.edit_text("Член команды удалён.")
    except Exception:
        pass


# ---------- Блог: описание страницы, добавление записей, список и редактирование ----------


@router.callback_query(SuperAdminCallbackFilter(), F.data == "blog_edit_page_description")
async def cb_blog_edit_page_description(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditBlogPageDescriptionFSM.description)
    await callback.message.answer("Введите новый текст описания страницы «Блог» (одним сообщением):")
    await callback.answer()


@router.message(EditBlogPageDescriptionFSM.description, F.text)
async def blog_page_description_save(message: Message, state: FSMContext) -> None:
    update_blog_page_description(message.text or "")
    await state.clear()
    await message.answer("Описание страницы «Блог» обновлено.")


@router.callback_query(SuperAdminCallbackFilter(), F.data == "blog_add")
async def cb_blog_add(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AddBlogPostFSM.photo)
    await callback.message.answer("Отправьте фото для записи (или текст «пропустить» без фото):")
    await callback.answer()


@router.message(AddBlogPostFSM.photo, F.photo)
async def blog_add_photo_photo(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await state.set_state(AddBlogPostFSM.description)
    await message.answer("Введите описание записи:")


@router.message(AddBlogPostFSM.photo, F.text)
async def blog_add_photo_skip(message: Message, state: FSMContext) -> None:
    if (message.text or "").strip().lower() in ("пропустить", "пропустить без фото", "-"):
        await state.update_data(photo="")
    await state.set_state(AddBlogPostFSM.description)
    await message.answer("Введите описание записи:")


@router.message(AddBlogPostFSM.description, F.text)
async def blog_add_description(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    data = await state.get_data()
    photo = data.get("photo", "")
    post_id = add_blog_post(text, photo)
    await state.clear()
    if post_id is not None:
        await message.answer(f"Запись блога добавлена (id={post_id}).")
    else:
        await message.answer("Ошибка при добавлении записи блога.")


@router.callback_query(F.data == "blog_list")
async def cb_blog_list(callback: CallbackQuery) -> None:
    """Показать все записи блога: фото, номер, описание + кнопки редактирования для супер-админа."""
    posts = get_all_blog_posts()
    if not posts:
        await callback.message.answer("Пока нет ни одной записи блога.")
        await callback.answer()
        return

    is_super_admin = callback.from_user and callback.from_user.id == SUPER_ADMIN_ID

    for pid, number, description, photo in posts:
        caption = (
            f"📽️ <b>Запись №{number}</b>\n"
            f"Описание: {description or '—'}"
        )
        keyboard = None
        if is_super_admin:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="✏️ Описание", callback_data=f"blog_edit_{pid}_description"),
                        InlineKeyboardButton(text="✏️ Фото", callback_data=f"blog_edit_{pid}_photo"),
                    ],
                ]
            )

        if photo:
            try:
                await callback.message.answer_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=keyboard,
                )
            except Exception:
                await callback.message.answer(caption, parse_mode="HTML", reply_markup=keyboard)
        else:
            await callback.message.answer(caption, parse_mode="HTML", reply_markup=keyboard)

    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data.startswith("blog_edit_"))
async def cb_blog_edit(callback: CallbackQuery, state: FSMContext) -> None:
    """Начать редактирование поля записи блога. callback_data = blog_edit_<id>_<field>."""
    parts = callback.data.split("_")
    if len(parts) != 4:
        await callback.answer()
        return
    _, _, pid_str, field = parts
    try:
        post_id = int(pid_str)
    except ValueError:
        await callback.answer()
        return
    if field not in ("description", "photo"):
        await callback.answer()
        return
    post = get_blog_post(post_id)
    if not post:
        await callback.answer("Запись блога не найдена.")
        return
    await state.update_data(blog_edit_post_id=post_id, blog_edit_field=field)
    await state.set_state(EditBlogPostFSM.value)
    prompts = {
        "description": "Введите новое описание записи (или «пропустить»):",
        "photo": "Отправьте новое фото (или текст «пропустить»):",
    }
    await callback.message.answer(prompts[field])
    await callback.answer()


@router.message(EditBlogPostFSM.value, F.photo)
async def blog_edit_value_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    pid = data.get("blog_edit_post_id")
    field = data.get("blog_edit_field")
    if field != "photo" or pid is None:
        await state.clear()
        return
    file_id = message.photo[-1].file_id
    post = get_blog_post(pid)
    if not post:
        await state.clear()
        await message.answer("Запись блога не найдена.")
        return
    _, number, description, _ = post
    update_blog_post(pid, number, description, file_id)
    await state.clear()
    await message.answer("Фото записи блога обновлено.")


@router.message(EditBlogPostFSM.value, F.text)
async def blog_edit_value_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    pid = data.get("blog_edit_post_id")
    field = data.get("blog_edit_field")
    if pid is None or field is None:
        await state.clear()
        return
    post = get_blog_post(pid)
    if not post:
        await state.clear()
        await message.answer("Запись блога не найдена.")
        return
    _, number, description, photo = post
    value = (message.text or "").strip()
    if value.lower() in ("пропустить", "-"):
        value = ""
    if field == "description":
        description = value
    elif field == "photo":
        photo = value
    update_blog_post(pid, number, description, photo)
    await state.clear()
    await message.answer("Запись блога обновлена.")


# ---------- Спонсоры: описание страницы, добавление, список и редактирование ----------


@router.callback_query(SuperAdminCallbackFilter(), F.data == "sponsors_edit_page_description")
async def cb_sponsors_edit_page_description(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditSponsorsPageDescriptionFSM.description)
    await callback.message.answer("Введите новый текст описания страницы «Спонсоры» (одним сообщением):")
    await callback.answer()


@router.message(EditSponsorsPageDescriptionFSM.description, F.text)
async def sponsors_page_description_save(message: Message, state: FSMContext) -> None:
    update_sponsors_page_description(message.text or "")
    await state.clear()
    await message.answer("Описание страницы «Спонсоры» обновлено.")


@router.callback_query(SuperAdminCallbackFilter(), F.data == "sponsor_add")
async def cb_sponsor_add(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AddSponsorFSM.photo)
    await callback.message.answer("Отправьте фото спонсора (или текст «пропустить» без фото):")
    await callback.answer()


@router.message(AddSponsorFSM.photo, F.photo)
async def sponsor_add_photo_photo(message: Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await state.set_state(AddSponsorFSM.subtitle)
    await message.answer("Введите подзаголовок (subtitle), например: Главный партнёр:")


@router.message(AddSponsorFSM.photo, F.text)
async def sponsor_add_photo_skip(message: Message, state: FSMContext) -> None:
    if (message.text or "").strip().lower() in ("пропустить", "пропустить без фото", "-"):
        await state.update_data(photo="")
    await state.set_state(AddSponsorFSM.subtitle)
    await message.answer("Введите подзаголовок (subtitle), например: Главный партнёр:")


@router.message(AddSponsorFSM.subtitle, F.text)
async def sponsor_add_subtitle(message: Message, state: FSMContext) -> None:
    await state.update_data(subtitle=(message.text or "").strip())
    await state.set_state(AddSponsorFSM.title)
    await message.answer("Введите название спонсора (title):")


@router.message(AddSponsorFSM.title, F.text)
async def sponsor_add_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=(message.text or "").strip())
    await state.set_state(AddSponsorFSM.description)
    await message.answer("Введите описание спонсора:")


@router.message(AddSponsorFSM.description, F.text)
async def sponsor_add_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=(message.text or "").strip())
    await state.set_state(AddSponsorFSM.status)
    await message.answer("Введите статус (целое число: -1 — без медали, 1 — gold, 2 — silver, 3 — bronze):")


@router.message(AddSponsorFSM.status, F.text)
async def sponsor_add_status(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    try:
        status = int(text)
    except ValueError:
        await message.answer("Статус должен быть целым числом (-1, 1, 2, 3).")
        return
    if status not in (-1, 1, 2, 3):
        await message.answer("Статус должен быть одним из: -1, 1, 2, 3.")
        return
    data = await state.get_data()
    photo = data.get("photo", "")
    subtitle = data.get("subtitle", "")
    title = data.get("title", "")
    description = data.get("description", "")
    sponsor_id = add_sponsor(photo, subtitle, title, description, status)
    await state.clear()
    if sponsor_id is not None:
        await message.answer(f"Спонсор «{title}» добавлен (id={sponsor_id}).")
    else:
        await message.answer("Ошибка при добавлении спонсора.")


@router.callback_query(F.data == "sponsor_list")
async def cb_sponsor_list(callback: CallbackQuery) -> None:
    """Показать всех спонсоров: фото, subtitle, title, description, статус + кнопки редактирования для супер-админа."""
    sponsors = get_all_sponsors()
    if not sponsors:
        await callback.message.answer("Пока нет ни одного спонсора.")
        await callback.answer()
        return

    is_super_admin = callback.from_user and callback.from_user.id == SUPER_ADMIN_ID

    for sid, photo, subtitle, title, description, status in sponsors:
        medal_text = {
            -1: "без медали",
            1: "gold",
            2: "silver",
            3: "bronze",
        }.get(status, "неизвестно")
        caption = (
            f"<b>{title}</b>\n"
            f"{subtitle or ''}\n\n"
            f"{description or '—'}\n\n"
            f"Статус: {medal_text} ({status})"
        )
        keyboard = None
        if is_super_admin:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="✏️ Фото", callback_data=f"sponsor_edit_{sid}_photo"),
                        InlineKeyboardButton(text="✏️ Subtitle", callback_data=f"sponsor_edit_{sid}_subtitle"),
                    ],
                    [
                        InlineKeyboardButton(text="✏️ Title", callback_data=f"sponsor_edit_{sid}_title"),
                        InlineKeyboardButton(text="✏️ Описание", callback_data=f"sponsor_edit_{sid}_description"),
                    ],
                    [
                        InlineKeyboardButton(text="✏️ Статус", callback_data=f"sponsor_edit_{sid}_status"),
                    ],
                ]
            )

        if photo:
            try:
                await callback.message.answer_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=keyboard,
                )
            except Exception:
                await callback.message.answer(caption, parse_mode="HTML", reply_markup=keyboard)
        else:
            await callback.message.answer(caption, parse_mode="HTML", reply_markup=keyboard)

    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data.startswith("sponsor_edit_"))
async def cb_sponsor_edit(callback: CallbackQuery, state: FSMContext) -> None:
    """Начать редактирование поля спонсора. callback_data = sponsor_edit_<id>_<field>."""
    parts = callback.data.split("_")
    if len(parts) != 4:
        await callback.answer()
        return
    _, _, sid_str, field = parts
    try:
        sponsor_id = int(sid_str)
    except ValueError:
        await callback.answer()
        return
    if field not in ("photo", "subtitle", "title", "description", "status"):
        await callback.answer()
        return
    sponsor = get_sponsor(sponsor_id)
    if not sponsor:
        await callback.answer("Спонсор не найден.")
        return
    await state.update_data(sponsor_edit_id=sponsor_id, sponsor_edit_field=field)
    await state.set_state(EditSponsorFSM.value)
    prompts = {
        "photo": "Отправьте новое фото спонсора (или текст «пропустить»):",
        "subtitle": "Введите новый subtitle (или «пропустить»):",
        "title": "Введите новый title (или «пропустить»):",
        "description": "Введите новое описание (или «пропустить»):",
        "status": "Введите новый статус (целое число: -1, 1, 2, 3):",
    }
    await callback.message.answer(prompts[field])
    await callback.answer()


@router.message(EditSponsorFSM.value, F.photo)
async def sponsor_edit_value_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    sid = data.get("sponsor_edit_id")
    field = data.get("sponsor_edit_field")
    if field != "photo" or sid is None:
        await state.clear()
        return
    file_id = message.photo[-1].file_id
    sponsor = get_sponsor(sid)
    if not sponsor:
        await state.clear()
        await message.answer("Спонсор не найден.")
        return
    _, _, subtitle, title, description, status = sponsor
    update_sponsor(sid, file_id, subtitle, title, description, status)
    await state.clear()
    await message.answer("Фото спонсора обновлено.")


@router.message(EditSponsorFSM.value, F.text)
async def sponsor_edit_value_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    sid = data.get("sponsor_edit_id")
    field = data.get("sponsor_edit_field")
    if sid is None or field is None:
        await state.clear()
        return
    sponsor = get_sponsor(sid)
    if not sponsor:
        await state.clear()
        await message.answer("Спонсор не найден.")
        return
    _, photo, subtitle, title, description, status = sponsor
    value = (message.text or "").strip()
    if field in ("subtitle", "title", "description", "photo") and value.lower() in ("пропустить", "-"):
        value = ""
    if field == "photo":
        photo = value
    elif field == "subtitle":
        subtitle = value
    elif field == "title":
        title = value
    elif field == "description":
        description = value
    elif field == "status":
        try:
            status = int(value)
        except ValueError:
            await message.answer("Статус должен быть целым числом (-1, 1, 2, 3).")
            return
        if status not in (-1, 1, 2, 3):
            await message.answer("Статус должен быть одним из: -1, 1, 2, 3.")
            return
    update_sponsor(sid, photo, subtitle, title, description, status)
    await state.clear()
    await message.answer("Данные спонсора обновлены.")


# ---------- Контакты: редактирование полей страницы и просмотр сообщений ----------


_CONTACTS_EDIT_CALLBACKS = (
    "contacts_edit_description",
    "contacts_edit_email",
    "contacts_edit_phone",
    "contacts_edit_address",
    "contacts_edit_telegram",
)
_CONTACTS_FIELD_PROMPTS = {
    "contacts_edit_description": "Введите новый текст описания страницы контактов:",
    "contacts_edit_email": "Введите новую почту:",
    "contacts_edit_phone": "Введите новый телефон:",
    "contacts_edit_address": "Введите новый адрес:",
    "contacts_edit_telegram": "Введите Telegram (например @phoenixfromlbsu):",
}
_CONTACTS_FIELD_NAMES = {
    "contacts_edit_description": "description",
    "contacts_edit_email": "email",
    "contacts_edit_phone": "phone",
    "contacts_edit_address": "address",
    "contacts_edit_telegram": "telegram",
}


@router.callback_query(SuperAdminCallbackFilter(), F.data.in_(_CONTACTS_EDIT_CALLBACKS))
async def cb_contacts_edit_field(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(contacts_edit_field=callback.data)
    await state.set_state(EditContactsPageFSM.value)
    await callback.message.answer(_CONTACTS_FIELD_PROMPTS[callback.data])
    await callback.answer()


@router.message(EditContactsPageFSM.value, F.text)
async def contacts_edit_value(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    cb = data.get("contacts_edit_field")
    if cb not in _CONTACTS_FIELD_NAMES:
        await state.clear()
        return
    row = get_contacts_page()
    if row is None:
        await state.clear()
        await message.answer("Данные контактов не найдены.")
        return
    description, email, phone, address, telegram = row
    value = (message.text or "").strip()
    field = _CONTACTS_FIELD_NAMES[cb]
    if field == "description":
        description = value
    elif field == "email":
        email = value
    elif field == "phone":
        phone = value
    elif field == "address":
        address = value
    elif field == "telegram":
        telegram = value
    update_contacts_page(description, email, phone, address, telegram)
    await state.clear()
    await message.answer("Контакты обновлены.")


@router.callback_query(SuperAdminCallbackFilter(), F.data == "contacts_messages")
async def cb_contacts_messages(callback: CallbackQuery) -> None:
    """Показать все сообщения с сайта: имя, почта, текст."""
    messages = get_all_contact_messages()
    if not messages:
        await callback.message.answer("Сообщений пока нет.")
        await callback.answer()
        return
    for mid, name, email, message_text, telegram_username, created_at in messages:
        telegram_line = f"<b>Telegram:</b> {telegram_username or '—'}\n" if telegram_username else ""
        text = (
            f"📩 <b>Сообщение #{mid}</b>\n"
            f"<b>Имя:</b> {name or '—'}\n"
            f"<b>Почта:</b> {email or '—'}\n"
            f"{telegram_line}"
            f"<b>Текст:</b>\n{message_text or '—'}\n"
            f"<i>{created_at}</i>"
        )
        await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


# ---------- Анкеты «Стать участником»: список и удаление ----------


@router.callback_query(SuperAdminCallbackFilter(), F.data == "join_edit_page_description")
async def cb_join_edit_page_description(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EditJoinPageDescriptionFSM.description)
    await callback.message.answer(
        "Введите новый текст описания страницы «Стать участником» (одним сообщением):"
    )
    await callback.answer()


@router.message(EditJoinPageDescriptionFSM.description, F.text)
async def join_page_description_save(message: Message, state: FSMContext) -> None:
    update_join_page_description(message.text or "")
    await state.clear()
    await message.answer("Описание страницы «Стать участником» обновлено.")


@router.callback_query(SuperAdminCallbackFilter(), F.data == "join_list")
async def cb_join_list(callback: CallbackQuery) -> None:
    """Показать все анкеты с кнопкой удаления."""
    applications = get_all_join_applications()
    if not applications:
        await callback.message.answer("Анкет пока нет.")
        await callback.answer()
        return
    for row in applications:
        app_id, full_name, grade, profile, email, telegram, role, experience, motivation, created_at = row
        telegram_line = f"\n<b>Telegram:</b> {telegram or '—'}" if telegram else ""
        text = (
            f"🧾 <b>Анкета #{app_id}</b>\n"
            f"<b>ФИО:</b> {full_name or '—'}\n"
            f"<b>Параллель:</b> {grade or '—'}\n"
            f"<b>Профиль:</b> {profile or '—'}\n"
            f"<b>Email:</b> {email or '—'}{telegram_line}\n"
            f"<b>Роль:</b> {role or '—'}\n\n"
            f"<b>Опыт:</b>\n{experience or '—'}\n\n"
            f"<b>Мотивация:</b>\n{motivation or '—'}\n\n"
            f"<i>{created_at}</i>"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"join_delete_{app_id}")],
            ]
        )
        await callback.message.answer(text, parse_mode="HTML", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data.startswith("join_delete_"))
async def cb_join_delete_ask(callback: CallbackQuery) -> None:
    """Спросить подтверждение удаления анкеты. callback_data = join_delete_<id>."""
    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.answer()
        return
    try:
        app_id = int(parts[2])
    except ValueError:
        await callback.answer()
        return
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да, удалить", callback_data=f"join_confirm_delete_{app_id}"),
                InlineKeyboardButton(text="Отмена", callback_data="join_cancel_delete"),
            ],
        ]
    )
    await callback.message.answer(
        f"Удалить анкету #{app_id}?",
        parse_mode="HTML",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(SuperAdminCallbackFilter(), F.data.startswith("join_confirm_delete_"))
async def cb_join_confirm_delete(callback: CallbackQuery) -> None:
    """Подтверждение удаления анкеты. callback_data = join_confirm_delete_<id>."""
    parts = callback.data.split("_")
    if len(parts) != 4:
        await callback.answer()
        return
    try:
        app_id = int(parts[3])
    except ValueError:
        await callback.answer()
        return
    delete_join_application(app_id)
    await callback.answer("Анкета удалена.")
    try:
        await callback.message.edit_text("Анкета удалена.")
    except Exception:
        pass


@router.callback_query(SuperAdminCallbackFilter(), F.data == "join_cancel_delete")
async def cb_join_cancel_delete(callback: CallbackQuery) -> None:
    await callback.answer("Отменено.")
    try:
        await callback.message.edit_text("Отменено.")
    except Exception:
        pass


@router.callback_query(SuperAdminCallbackFilter(), F.data == "team_cancel_delete")
async def cb_team_cancel_delete(callback: CallbackQuery) -> None:
    await callback.answer("Отменено.")
    try:
        await callback.message.edit_text("Отменено.")
    except Exception:
        pass
