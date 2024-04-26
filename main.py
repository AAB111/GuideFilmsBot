from aiogram import Bot, Dispatcher, types

from config import settings
import sys
from aiogram.filters import CommandStart
import asyncio
import logging

from handlers.search import search_router
from handlers.review import review_router
from handlers.card import card_router
from api.requests import request_auth

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    welcome_text = (
        f"Привет, {message.from_user.full_name}! Добро пожаловать в мир фильмов! 🎬\n\n"
        "Я - ваш проводник в этом удивительном мире.\n"
        "Моя задача - помочь вам найти лучшие фильмы для просмотра и наслаждения.\n"
        "Спросите меня о популярных фильмах или составьте свой фильм.\n"
        "Если у вас есть описание фильма, который вы ищете, просто дайте мне знать, и я найду для вас похожие фильмы!\n"
        "И помните, я всегда здесь, чтобы помочь вам в выборе фильма для вашего вечера! 🍿"
        "Доступные команды:\n"
        "/card - получить информацию о конкретном фильме\n"
    )
    await message.answer(welcome_text)
    await request_auth(message.from_user.id)


async def main():
    bot = Bot(token=settings.API_TG_BOT_TOKEN)
    dp.include_router(review_router)
    dp.include_router(card_router)
    dp.include_router(search_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
