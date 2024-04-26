from aiogram import Router, types
from handlers.functions_common import show_group_movies
from api.requests import get_search_movies

search_router = Router()


@search_router.message()
async def search_start(message: types.Message):
    send_message = await message.reply("Ищу ищу 👀")
    overview = message.text
    movies = await get_search_movies(overview, message.from_user.id)
    try:
        if movies:
            await show_group_movies(movies, send_message)
        else:
            await send_message.edit_text("К сожалению, ничего не найдено. Попробуйте составить запрос заново.")
    except Exception as e:
        await send_message.edit_text("Произошла непредвиденная ошибка. Попробуйте составить запрос заново.")
