from aiogram.types import Message, CallbackQuery
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any
import time
import asyncio

from config import SUPER_ADMIN_ID
from db.queries.user_queries import get_allowed_user_ids


def _user_id_from_event(event: Message | CallbackQuery) -> int | None:
    if event.from_user is None:
        return None
    return event.from_user.id


def _is_start_message(event: Message | CallbackQuery) -> bool:
    return isinstance(event, Message) and event.text is not None and event.text.strip().startswith("/start")


class AccessControlMiddleware(BaseMiddleware):
    """
    Централизованная проверка доступа:
    - /start всегда пропускается (хендлер сам решит: нет в БД → «Нет доступа»).
    - Супер-админ всегда пропускается.
    - Остальные — только если user_id есть в таблице users.
    """

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Any],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user_id = _user_id_from_event(event)
        if user_id is None:
            return await handler(event, data)

        if _is_start_message(event):
            return await handler(event, data)
        if user_id == SUPER_ADMIN_ID:
            return await handler(event, data)

        allowed_ids = get_allowed_user_ids()
        if user_id in allowed_ids:
            return await handler(event, data)

        text = "У вас нет доступа к боту."
        if isinstance(event, Message):
            await event.answer(text)
        elif isinstance(event, CallbackQuery):
            await event.message.reply(text)
        return


class ThrottledMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: float = 1.0):
        self.limit = limit_seconds
        self.timestamps = {}

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Any],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user_id = _user_id_from_event(event)
        if user_id is None:
            return await handler(event, data)

        now = time.monotonic()
        last_time = self.timestamps.get(user_id, 0)

        if now - last_time < self.limit:
            if isinstance(event, Message):
                msg = await event.answer("Слишком часто. Подожди немного.")
                await asyncio.sleep(2)
                await msg.delete()
            return

        self.timestamps[user_id] = now
        return await handler(event, data)


def is_user_registered(user_id: int) -> bool:
    """Пользователь в таблице users (разрешённый доступ). Супер-админ не обязан быть в таблице."""
    if user_id == SUPER_ADMIN_ID:
        return True
    return user_id in get_allowed_user_ids()
