"""
Запросы к таблицам team_page (описание страницы) и team_members (члены команды).
"""
from db.connection import fetch_from_db


# ---------- team_page ----------


def get_team_page_description() -> str:
    """Возвращает описание страницы «Команда» или пустую строку."""
    result = fetch_from_db("SELECT description FROM team_page WHERE id = 1")
    if not result or len(result) == 0:
        return ""
    return result[0][0] or ""


def update_team_page_description(description: str) -> None:
    """Обновляет описание страницы «Команда»."""
    fetch_from_db(
        "UPDATE team_page SET description = %s WHERE id = 1",
        (description,),
    )


# ---------- team_members ----------


def get_all_team_members() -> list[tuple[int, str, str, str, str, str]]:
    """Список всех: (id, name, specialty, description, status, photo)."""
    result = fetch_from_db(
        "SELECT id, name, specialty, description, status, photo FROM team_members ORDER BY id"
    )
    if not result:
        return []
    return [tuple(row) for row in result]


def get_team_member(member_id: int) -> tuple[int, str, str, str, str, str] | None:
    """Один член по id: (id, name, specialty, description, status, photo)."""
    result = fetch_from_db(
        "SELECT id, name, specialty, description, status, photo FROM team_members WHERE id = %s",
        (member_id,),
    )
    if not result or len(result) == 0:
        return None
    row = result[0]
    return (row[0], row[1], row[2], row[3], row[4], row[5])


def add_team_member(name: str, specialty: str, description: str, status: str, photo: str) -> int | None:
    """Добавляет члена команды. Возвращает id новой записи или None."""
    result = fetch_from_db(
        """
        INSERT INTO team_members (name, specialty, description, status, photo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (name, specialty, description, status, photo),
    )
    if result is None:
        return None
    return result[0]


def update_team_member(
    member_id: int,
    name: str,
    specialty: str,
    description: str,
    status: str,
    photo: str,
) -> None:
    """Обновляет члена команды по id."""
    fetch_from_db(
        """
        UPDATE team_members
        SET name = %s, specialty = %s, description = %s, status = %s, photo = %s
        WHERE id = %s
        """,
        (name, specialty, description, status, photo, member_id),
    )


def delete_team_member(member_id: int) -> None:
    """Удаляет члена команды по id."""
    fetch_from_db("DELETE FROM team_members WHERE id = %s", (member_id,))
