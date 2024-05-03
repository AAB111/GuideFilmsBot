from aiogram import Router, types, F
from aiogram.filters import Command
from api.requests import get_content_based
from handlers.functions_common import show_group_movies, show_text_movies

content_router = Router()


@content_router.message(Command('content'))
async def start_content(message: types.Message):
    movies = await get_content_based(message.from_user.id, {"page": 1, "n": 100})
    if movies is not None:
        if len(movies) > 0:
            media = await show_group_movies(movies)
            movies_poster_path_none = list(filter(lambda movie: movie['poster_path'] is None, movies))
            await message.reply(text="Похоже на то, что вам интересно! 😊")
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
        else:
            await message.reply("К сожалению, ничего не найдено.")
        return
    await message.reply("Внутренняя ошибка. Уже исправляем.")
