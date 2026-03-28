"""
Запросы к таблице about_page (одна строка: описание, годы в соревнованиях, размер команды).
"""
from db.connection import fetch_from_db


def get_about_page() -> tuple[str, int, int] | None:
    """Возвращает (description, years_in_competitions, team_size) или None."""
    result = fetch_from_db(
        "SELECT description, years_in_competitions, team_size FROM about_page WHERE id = 1"
    )
    if not result or len(result) == 0:
        return None
    row = result[0]
    return (row[0], row[1], row[2])


def update_about_page(description: str, years_in_competitions: int, team_size: int) -> None:
    """Обновляет единственную запись блока «Про нас»."""
    fetch_from_db(
        """
        UPDATE about_page
        SET description = %s, years_in_competitions = %s, team_size = %s
        WHERE id = 1
        """,
        (description, years_in_competitions, team_size),
    )
