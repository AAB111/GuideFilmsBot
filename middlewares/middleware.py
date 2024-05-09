from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any
from api.requests import check_user


class CheckUserMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if await check_user(event.from_user.id) == 404:
            await event.answer("Такого пользователя не существует. Попробуйте /start")
            return
        return await handler(event, data)
