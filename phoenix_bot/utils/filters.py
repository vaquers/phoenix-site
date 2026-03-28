"""
Централизованные проверки доступа для хендлеров.
"""
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config import SUPER_ADMIN_ID
from db.queries.user_queries import get_user, get_allowed_user_ids


def is_super_admin(user_id: int) -> bool:
    return user_id == SUPER_ADMIN_ID


def is_allowed_user(user_id: int) -> bool:
    """Пользователь в таблице users или супер-админ (доступ разрешён)."""
    if is_super_admin(user_id):
        return True
    return user_id in get_allowed_user_ids()


class SuperAdminFilter(BaseFilter):
    """Фильтр: только супер-админ (для message)."""

    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id == SUPER_ADMIN_ID


class SuperAdminCallbackFilter(BaseFilter):
    """Фильтр: только супер-админ (для callback_query)."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.from_user is not None and callback.from_user.id == SUPER_ADMIN_ID


class AllowedUserFilter(BaseFilter):
    """Фильтр: пользователь есть в users или супер-админ."""

    async def __call__(self, message: Message) -> bool:
        if message.from_user is None:
            return False
        return is_allowed_user(message.from_user.id)
