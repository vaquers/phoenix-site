"""
Запросы к таблицам sponsors_page (описание страницы) и sponsors (список спонсоров).
"""
from db.connection import fetch_from_db


# ---------- sponsors_page ----------


def get_sponsors_page_description() -> str:
    """Возвращает описание страницы «Спонсоры» или пустую строку."""
    result = fetch_from_db("SELECT description FROM sponsors_page WHERE id = 1")
    if not result or len(result) == 0:
        return ""
    return result[0][0] or ""


def update_sponsors_page_description(description: str) -> None:
    """Обновляет описание страницы «Спонсоры»."""
    fetch_from_db(
        "UPDATE sponsors_page SET description = %s WHERE id = 1",
        (description,),
    )


# ---------- sponsors ----------


def get_all_sponsors() -> list[tuple[int, str, str, str, int]]:
    """
    Список всех спонсоров.
    Порядок: gold (1), silver (2), bronze (3), остальные (status = -1).
    Возвращает список кортежей: (id, photo, subtitle, title, description, status).
    """
    result = fetch_from_db(
        """
        SELECT id, photo, subtitle, title, description, status
        FROM sponsors
        ORDER BY CASE status WHEN 1 THEN 0 WHEN 2 THEN 1 WHEN 3 THEN 2 ELSE 3 END, id
        """
    )
    if not result:
        return []
    return [tuple(row) for row in result]


def get_sponsor(sponsor_id: int) -> tuple[int, str, str, str, int] | None:
    """Один спонсор по id: (id, photo, subtitle, title, description, status)."""
    result = fetch_from_db(
        "SELECT id, photo, subtitle, title, description, status FROM sponsors WHERE id = %s",
        (sponsor_id,),
    )
    if not result or len(result) == 0:
        return None
    row = result[0]
    return (row[0], row[1], row[2], row[3], row[4], row[5])


def add_sponsor(photo: str, subtitle: str, title: str, description: str, status: int) -> int | None:
    """Добавляет спонсора. Возвращает id новой записи или None."""
    result = fetch_from_db(
        """
        INSERT INTO sponsors (photo, subtitle, title, description, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (photo, subtitle, title, description, status),
    )
    if result is None:
        return None
    return result[0]


def update_sponsor(
    sponsor_id: int,
    photo: str,
    subtitle: str,
    title: str,
    description: str,
    status: int,
) -> None:
    """Обновляет спонсора по id."""
    fetch_from_db(
        """
        UPDATE sponsors
        SET photo = %s, subtitle = %s, title = %s, description = %s, status = %s
        WHERE id = %s
        """,
        (photo, subtitle, title, description, status, sponsor_id),
    )

