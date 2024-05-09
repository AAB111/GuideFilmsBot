from aiogram import Router, types
from aiogram.filters import Command
from api.requests import get_content_based
from handlers.functions_common import show_group_movies_message, show_text_movies
from kbrds.keyboards import create_transition_inline

content_router = Router()


@content_router.message(Command('content'))
async def start_content(message: types.Message):
    movies = await get_content_based(message.from_user.id, {"page": 1, "n": 20})
    await show_group_movies_message(message, movies, 'Вам должно понравиться')