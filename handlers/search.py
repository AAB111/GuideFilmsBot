from aiogram import Router, types
from handlers.functions_common import show_group_movies_message, show_text_movies
from api.requests import get_search_movies
from kbrds.keyboards import create_transition_inline

search_router = Router()


@search_router.message()
async def start_search(message: types.Message):
    await message.reply("Ищу ищу 👀")
    overview = message.text
    movies = await get_search_movies(overview)
    await show_group_movies_message(message, movies, 'Вот что я нашел!')
