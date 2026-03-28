"""
Команды управления доступом: только супер-админ.
/add_user <user_id> [user_id ...] — добавить пользователей (is_admin=False).
/set_admin <user_id> <0|1> — выставить is_admin (0 — снять, 1 — назначить).
"""
import re
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.filters import SuperAdminFilter
from db.queries.user_queries import add_user, set_admin, user_exists

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
