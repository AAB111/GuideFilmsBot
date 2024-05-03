from aiogram import Router, types
from handlers.functions_common import show_group_movies, show_text_movies
from api.requests import get_search_movies

search_router = Router()


@search_router.message()
async def start_search(message: types.Message):
    await message.reply("Ищу ищу 👀")
    overview = message.text
    movies = await get_search_movies(overview, message.from_user.id)
    if movies is not None:
        if len(movies) > 0:
            media = await show_group_movies(movies)
            movies_poster_path_none = list(filter(lambda movie: movie['poster_path'] is None, movies))
            if len(media) > 0:
                num_batches = len(media) // 10 + (len(media) % 10 > 0)
                for i in range(num_batches):
                    start_index = i * 10
                    end_index = (i + 1) * 10
                    await message.reply_media_group(media=media[start_index:end_index])
            if len(movies_poster_path_none) > 0:
                text_message = await show_text_movies(movies_poster_path_none)
                await message.reply(text_message, parse_mode="HTML")
        else:
            await message.reply("К сожалению, ничего не найдено. Попробуйте составить запрос позже.")
        return
    await message.reply("Внутренняя ошибка. Уже исправляем.")
