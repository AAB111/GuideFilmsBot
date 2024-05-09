from aiogram import Router, types
from aiogram.filters import Command
from api.requests import (get_movie_from_list)
from handlers.functions_common import show_group_movies_message

be_watching_router = Router()


@be_watching_router.message(Command('tabs'))
async def get_be_watching(message: types.Message):
    result = await get_movie_from_list("be_watching", {"user_id": message.from_user.id})
    if result['status'] == 200:
        result['data'] = [movie['movie'] for movie in result['data']]
    await show_group_movies_message(message, result, "Ваши закладки")
