"""
Запросы к таблицам contacts_page (описание страницы, почта, телефон, адрес, телеграм)
и contact_messages (сообщения с сайта).
"""
from db.connection import fetch_from_db


# ---------- contacts_page ----------


def get_contacts_page() -> tuple[str, str, str, str, str] | None:
    """
    Возвращает одну запись страницы контактов или None.
    (description, email, phone, address, telegram)
    """
    result = fetch_from_db(
        "SELECT description, email, phone, address, telegram FROM contacts_page WHERE id = 1"
    )
    if not result or len(result) == 0:
        return None
    row = result[0]
    return (row[0] or "", row[1] or "", row[2] or "", row[3] or "", row[4] or "")


def update_contacts_page(
    description: str,
    email: str,
    phone: str,
    address: str,
    telegram: str,
) -> None:
    """Обновляет запись страницы контактов."""
    fetch_from_db(
        """
        UPDATE contacts_page
        SET description = %s, email = %s, phone = %s, address = %s, telegram = %s
        WHERE id = 1
        """,
        (description, email, phone, address, telegram),
    )


# ---------- contact_messages ----------


def get_all_contact_messages() -> list[tuple[int, str, str, str, str, str]]:
    """
    Список всех сообщений: (id, name, email, message_text, telegram_username, created_at_str).
    created_at отдаём как строку для отображения.
    """
    result = fetch_from_db(
        "SELECT id, name, email, message_text, telegram_username, created_at::text FROM contact_messages ORDER BY created_at DESC"
    )
    if not result:
        return []
    return [tuple(row) for row in result]


def add_contact_message(name: str, email: str, message_text: str, telegram_username: str = "") -> int | None:
    """Добавляет сообщение. Возвращает id или None."""
    result = fetch_from_db(
        """
        INSERT INTO contact_messages (name, email, message_text, telegram_username)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (name, email, message_text, (telegram_username or "").strip()),
    )
    if result is None:
        return None
    return result[0]
