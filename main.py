from aiogram import Bot, Dispatcher, types

from config import settings
import sys
from aiogram.filters import CommandStart
import asyncio
import logging
from handlers.pop import pop_router
from handlers.content import content_router
from handlers.search import search_router
from handlers.review import review_router
from handlers.card import card_router
from handlers.be_watching import be_watching_router
from handlers.transition import transition_router
from api.requests import request_auth
from middlewares.middleware import CheckUserMiddleware

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    welcome_text = (
        f"Привет, {message.from_user.full_name}! Добро пожаловать в мир фильмов! 🎬\n\n"
        "Я - ваш проводник в этом удивительном мире.\n"
        "Моя задача - помочь вам найти лучшие фильмы для просмотра и наслаждения.\n"
        "Спросите меня о популярных фильмах или составьте свой фильм.\n"
        "Если у вас есть описание фильма, который вы ищете, просто дайте мне знать, и я найду для вас похожие фильмы!\n"
        "И помните, я всегда здесь, чтобы помочь вам в выборе фильма для вашего вечера! 🍿\n\n"
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/pop - получить информацию о популярных фильмах\n"
        "/content - получить фильмы под ваши интересы\n"
        "/card - получить информацию о конкретном фильме\n"
        "/tabs - закладки ваших фильмов\n"
    )
    status = await request_auth(message.from_user.id)
    if status == 500 or status is None:
        await message.answer('Что-то пошло не так. Попробуйте /start позже.')
        return
    await message.answer(welcome_text)


async def main():
    bot = Bot(token=settings.API_TG_BOT_TOKEN)
    dp.callback_query.middleware(CheckUserMiddleware())
    pop_router.message.middleware(CheckUserMiddleware())
    content_router.message.middleware(CheckUserMiddleware())
    transition_router.message.middleware(CheckUserMiddleware())
    review_router.message.middleware(CheckUserMiddleware())
    be_watching_router.message.middleware(CheckUserMiddleware())
    card_router.message.middleware(CheckUserMiddleware())
    search_router.message.middleware(CheckUserMiddleware())
    dp.include_router(pop_router)
    dp.include_router(content_router)
    dp.include_router(transition_router)
    dp.include_router(review_router)
    dp.include_router(be_watching_router)
    dp.include_router(card_router)
    dp.include_router(search_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
