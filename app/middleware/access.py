import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.config import config

logger = logging.getLogger(__name__)


class AccessControlMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = getattr(event, "from_user", None)
        if user is not None and user.id != config.owner_id:
            logger.warning("Access denied for user %s (@%s)", user.id, user.username)

            if isinstance(event, Message):
                await event.answer("⛔ Access denied. You are not authorized.")
            elif isinstance(event, CallbackQuery):
                await event.answer("⛔ Access denied", show_alert=True)

            return None

        return await handler(event, data)
