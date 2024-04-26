from aiogram import Router, types, F
from aiogram.filters import Command
from api.requests import (get_movie_from_list)
from handlers.functions_common import show_group_movies

be_watching_router = Router()


@be_watching_router.message(Command('be_watching'))
async def be_watching(message: types.Message):
    movies = await get_movie_from_list("be_watching", {"user_id": message.from_user.id})
    if movies is not None:
        await show_group_movies(movies, message)
    else:
        await message.reply("В списке пусто.")
