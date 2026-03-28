"""
Запросы к таблицам join_page (описание страницы) и join_applications (анкеты).
"""
from db.connection import fetch_from_db


# ---------- join_page ----------


def get_join_page_description() -> str:
    """Возвращает описание страницы «Стать участником»."""
    result = fetch_from_db("SELECT description FROM join_page WHERE id = 1")
    if not result or len(result) == 0:
        return ""
    return (result[0][0] or "").strip()


def update_join_page_description(description: str) -> None:
    """Обновляет описание страницы «Стать участником»."""
    fetch_from_db("UPDATE join_page SET description = %s WHERE id = 1", (description or "",))


# ---------- join_applications ----------


def get_all_join_applications() -> list[tuple]:
    """
    Список всех анкет: (id, full_name, grade, profile, email, telegram, role, experience, motivation, created_at_str).
    """
    result = fetch_from_db(
        """
        SELECT id, full_name, grade, profile, email, telegram, role, experience, motivation, created_at::text
        FROM join_applications
        ORDER BY created_at DESC
        """
    )
    if not result:
        return []
    return [tuple(row) for row in result]


def add_join_application(
    full_name: str,
    grade: str,
    profile: str,
    email: str,
    telegram: str,
    role: str,
    experience: str,
    motivation: str,
) -> int | None:
    """Добавляет анкету. Возвращает id или None."""
    result = fetch_from_db(
        """
        INSERT INTO join_applications (full_name, grade, profile, email, telegram, role, experience, motivation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            (full_name or "").strip(),
            (grade or "").strip(),
            (profile or "").strip(),
            (email or "").strip(),
            (telegram or "").strip(),
            (role or "").strip(),
            (experience or "").strip(),
            (motivation or "").strip(),
        ),
    )
    if result is None:
        return None
    return result[0]


def delete_join_application(app_id: int) -> bool:
    """Удаляет анкету по id. Возвращает True если удалено."""
    result = fetch_from_db("DELETE FROM join_applications WHERE id = %s", (app_id,))
    return result is not None
