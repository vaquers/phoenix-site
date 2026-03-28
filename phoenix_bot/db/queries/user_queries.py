"""
Запросы к таблице users (user_id BIGINT PRIMARY KEY, is_admin BOOLEAN).
Пользователи добавляются только супер-админом, авто-сохранения нет.
"""
from db.connection import fetch_from_db


def get_user(user_id: int) -> tuple | None:
    """Возвращает (user_id, is_admin) или None, если пользователя нет."""
    result = fetch_from_db(
        "SELECT user_id, is_admin FROM users WHERE user_id = %s",
        (user_id,),
    )
    if not result or len(result) == 0:
        return None
    row = result[0]
    return (row[0], row[1])


def get_allowed_user_ids() -> list[int]:
    """Список user_id всех пользователей, которым разрешён доступ (для middleware)."""
    result = fetch_from_db("SELECT user_id FROM users")
    if not result:
        return []
    return [row[0] for row in result]


def add_user(user_id: int, is_admin: bool = False) -> None:
    """
    Добавляет пользователя. Если уже есть — не перезаписывает (ON CONFLICT DO NOTHING).
    """
    fetch_from_db(
        """
        INSERT INTO users (user_id, is_admin) VALUES (%s, %s)
        ON CONFLICT (user_id) DO NOTHING
        """,
        (user_id, is_admin),
    )


def set_admin(user_id: int, is_admin: bool) -> None:
    """Устанавливает is_admin для существующего пользователя."""
    fetch_from_db(
        "UPDATE users SET is_admin = %s WHERE user_id = %s",
        (is_admin, user_id),
    )


def user_exists(user_id: int) -> bool:
    """Проверяет, есть ли пользователь в таблице."""
    return get_user(user_id) is not None
