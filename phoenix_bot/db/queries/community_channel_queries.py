"""
Посты канала сообщества: сохранение при channel_post и выборка для API.
"""
from db.connection import fetch_from_db


def add_channel_post(channel_username: str, message_id: int, link: str, title: str) -> bool:
    """
    Добавляет пост канала (по id сообщения). При дубликате (channel_username, message_id) — обновляет title/link.
    """
    result = fetch_from_db(
        """
        INSERT INTO community_channel_posts (channel_username, message_id, link, title)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (channel_username, message_id)
        DO UPDATE SET link = EXCLUDED.link, title = EXCLUDED.title, created_at = NOW()
        """,
        (channel_username, message_id, link, title),
    )
    return result is not None


def get_last_channel_posts(channel_username: str, limit: int = 3) -> list[tuple[int, str, str]]:
    """
    Последние посты канала для API: (message_id, link, title).
    Сравнение channel_username без учёта регистра.
    """
    uname = (channel_username or "").strip().lower()
    result = fetch_from_db(
        """
        SELECT message_id, link, title
        FROM community_channel_posts
        WHERE LOWER(channel_username) = %s
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (uname, limit),
    )
    if not result:
        return []
    return [tuple(row) for row in result]


def trim_channel_posts(channel_username: str, keep: int = 15) -> None:
    """Оставляет только последние keep постов по дате, остальные удаляет."""
    uname = (channel_username or "").strip().lower()
    fetch_from_db(
        """
        DELETE FROM community_channel_posts
        WHERE LOWER(channel_username) = %s
          AND id IN (
            SELECT id FROM community_channel_posts
            WHERE LOWER(channel_username) = %s
            ORDER BY created_at DESC
            OFFSET %s
          )
        """,
        (uname, uname, keep),
    )
