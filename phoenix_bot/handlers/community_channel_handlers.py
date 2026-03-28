"""
Обработка постов канала сообщества: сохраняем в БД для страницы «Сообщество».
Бот должен быть добавлен в канал как администратор.
"""
from aiogram import Router
from aiogram.types import Message

from config import COMMUNITY_CHANNEL_USERNAME
from db.queries.community_channel_queries import add_channel_post, trim_channel_posts


router = Router(name="community_channel")


def _make_title(msg: Message, max_len: int = 200) -> str:
    """Берём текст или подпись поста, обрезаем до max_len."""
    raw = (msg.text or msg.caption or "").strip()
    if not raw:
        return "Пост"
    return (raw[: max_len] + "…") if len(raw) > max_len else raw


@router.channel_post()
@router.edited_channel_post()
async def on_channel_post(msg: Message) -> None:
    """Сохраняем пост канала в БД, если это наш канал сообщества."""
    chat = msg.chat
    username = (chat.username or "").strip().lower()
    if not username or username != COMMUNITY_CHANNEL_USERNAME.lower():
        return
    # В БД храним username в нижнем регистре, чтобы выборка не зависела от регистра
    link = f"https://t.me/{chat.username}/{msg.message_id}"
    title = _make_title(msg)
    add_channel_post(username, msg.message_id, link, title)
    trim_channel_posts(username, keep=15)
