from aiogram import Router, types
from aiogram.filters import Command
from api.requests import get_pop_based
from handlers.functions_common import show_group_movies_message

pop_router = Router()


@pop_router.message(Command('pop'))
async def start_pop(message: types.Message):
    result = await get_pop_based()
    await show_group_movies_message(message, result, "Посмотрите популярные фильмы!")
