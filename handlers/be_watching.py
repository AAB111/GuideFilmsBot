from aiogram import Router, types, F
from aiogram.filters import Command
from api.requests import (get_movie_from_list)
from handlers.functions_common import show_group_movies, show_text_movies

be_watching_router = Router()


@be_watching_router.message(Command('tabs'))
async def get_be_watching(message: types.Message):
    movies = await get_movie_from_list("be_watching", {"user_id": message.from_user.id})
    if movies is not None:
        if len(movies) == 0:
            await message.reply("В списке пусто.")
            return
        movies = [movie['movie'] for movie in movies]
        movies_poster_path_none = list(filter(lambda movie: movie['poster_path'] is None, movies))
        media = await show_group_movies(movies)
        if len(media) > 0:
            num_batches = len(media) // 10 + (len(media) % 10 > 0)
            for i in range(num_batches):
                start_index = i * 10
                end_index = (i + 1) * 10
                await message.reply_media_group(media=media[start_index:end_index])
        if len(movies_poster_path_none) > 0:
            text_message = await show_text_movies(movies_poster_path_none)
            await message.reply(text_message, parse_mode="HTML")
        return
    await message.reply("Что-то пошло не так. Попробуйте /start снова.")
