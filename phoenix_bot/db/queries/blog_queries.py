"""
Запросы к таблицам blog_page (описание страницы) и blog_posts (записи блога).
"""
from db.connection import fetch_from_db


# ---------- blog_page ----------


def get_blog_page_description() -> str:
    """Возвращает описание страницы «Блог» или пустую строку."""
    result = fetch_from_db("SELECT description FROM blog_page WHERE id = 1")
    if not result or len(result) == 0:
        return ""
    return result[0][0] or ""


def update_blog_page_description(description: str) -> None:
    """Обновляет описание страницы «Блог»."""
    fetch_from_db(
        "UPDATE blog_page SET description = %s WHERE id = 1",
        (description,),
    )


# ---------- blog_posts ----------


def get_all_blog_posts() -> list[tuple[int, int, str, str]]:
    """
    Список всех записей блога.
    Возвращает список кортежей: (id, number, description, photo).
    """
    result = fetch_from_db(
        "SELECT id, number, description, photo FROM blog_posts ORDER BY number, id"
    )
    if not result:
        return []
    return [tuple(row) for row in result]


def get_blog_post(post_id: int) -> tuple[int, int, str, str] | None:
    """Одна запись по id: (id, number, description, photo)."""
    result = fetch_from_db(
        "SELECT id, number, description, photo FROM blog_posts WHERE id = %s",
        (post_id,),
    )
    if not result or len(result) == 0:
        return None
    row = result[0]
    return (row[0], row[1], row[2], row[3])


def add_blog_post(description: str, photo: str) -> int | None:
    """
    Добавляет запись блога.
    Номер записи выставляется автоматически как (MAX(number) + 1).
    Возвращает id новой записи или None.
    """
    result = fetch_from_db(
        """
        INSERT INTO blog_posts (number, description, photo)
        VALUES (
            COALESCE((SELECT MAX(number) FROM blog_posts), 0) + 1,
            %s,
            %s
        )
        RETURNING id
        """,
        (description, photo),
    )
    if result is None:
        return None
    return result[0]


def update_blog_post(
    post_id: int,
    number: int,
    description: str,
    photo: str,
) -> None:
    """Обновляет запись блога по id."""
    fetch_from_db(
        """
        UPDATE blog_posts
        SET number = %s, description = %s, photo = %s
        WHERE id = %s
        """,
        (number, description, photo, post_id),
    )

