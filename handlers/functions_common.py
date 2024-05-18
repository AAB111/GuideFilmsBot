from aiogram import types
from aiogram.types import InputMediaPhoto

from api.requests import get_credits_by_id
from kbrds.keyboards import create_card_inline, create_transition_inline

MAX_TEXT_LENGTH = 1000


async def show_group_movies_message(message: types.Message, result, message_test):
    if result['status'] == 200 and result['data'] is not None:
        movies = result['data']
        if len(movies) > 0:
            media = await show_group_movies(movies)
            movies_poster_path_none = list(filter(lambda movie: movie['poster_path'] is None, movies))
            await message.reply(text=message_test)
            if len(media) > 0:
                num_batches = len(media) // 10 + (len(media) % 10 > 0)
                for i in range(num_batches):
                    start_index = i * 10
                    end_index = (i + 1) * 10
                    await message.reply_media_group(media=media[start_index:end_index])
            if len(movies_poster_path_none) > 0:
                text_message = await show_text_movies(movies_poster_path_none)
                await message.reply(text_message, parse_mode="HTML")

            kbrds = create_transition_inline(movies)
            for kbrd in kbrds:
                await message.reply(text="Что вы хотите посмотреть?", reply_markup=kbrd)
            return
        else:
            await message.reply("К сожалению, ничего не найдено.")
        return
    elif result['status'] == 404:
        await message.reply("К сожалению, ничего не найдено.")
        return
    await message.reply("Внутренняя ошибка. Уже исправляем.")


async def show_group_movies(movies):
    if movies is None:
        return []
    media = []
    for movie in movies:
        if movie['poster_path'] is not None:
            post_url = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
            title = movie['title']
            overview = movie['overview']
            post_text = f"{title}\n{overview}"
            media.append(InputMediaPhoto(media=post_url, caption=post_text))
    return media


async def show_text_movies(movies):
    top_5_message = "<b>Посмотри что нашёл</b>\n\n"
    for movie in movies:
        top_5_message += f"<b>{movie['title']}</b>:\n{movie['overview']}\n\n"
    return top_5_message


def truncate_text(text):
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]
        last_dot_index = text.rfind('.')
        if last_dot_index != -1:
            return text[:last_dot_index + 1]
    return text


async def send_movie_card(message: types.Message, result: dict):
    try:
        if (result['status'] != 200) or (result['data'] == {}):
            await message.reply("К сожалению, ничего не найдено. Попробуйте заново.")
            return
        movie = result['data']
        title = movie['title'].strip()
        overview = movie['overview'].strip()
        release_date = movie['release_date']
        vote_average = round(movie['vote_average'], 1)
        poster_path = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"

        genres = ', '.join(genre['genre']['name'].strip() for genre in movie['genres'])
        companies = ', '.join(company['company']['name'].strip() for company in movie['companies'])

        result = await get_credits_by_id(movie['id'])
        if result['status'] == 200 and result['data'] is not None:
            credits = result['data']
            directors = [crew_member['person']['name'].strip() for crew_member in credits[0]['crew'] if
                         crew_member['job'].strip() == 'Директор']
            top_cast = sorted(credits[0]['cast'], key=lambda x: x['person']['popularity'], reverse=True)[:6]
            actors = [cast_member['person']['name'].strip() for cast_member in top_cast]

            directors_text = ", ".join(directors)
            actors_text = ", ".join(actors)
            card_text = f"<b>{title}</b>\n\n" \
                        f"<i>Дата выхода 📅:</i> {release_date}\n" \
                        f"<i>Жанры 🎬:</i> {genres}\n" \
                        f"<i>Компании 💼:</i> {companies}\n" \
                        f"<i>Рейтинг:</i> {vote_average} ⭐️\n\n" \
                        f"<i>Режиссер(ы) 👨‍🎬:</i> {directors_text}\n\n" \
                        f"<i>В главных ролях 🌟:</i> {actors_text}\n\n" \
                        f"{overview}"
        else:
            card_text = f"<b>{title}</b>\n\n" \
                        f"<i>Дата выхода:</i> {release_date}\n" \
                        f"<i>Жанры:</i> {genres}\n" \
                        f"<i>Компании:</i> {companies}\n\n" \
                        f"{overview}"
        card_text = truncate_text(card_text)
        card_inline = create_card_inline(movie['id'])
        if movie['poster_path'] is not None:
            await message.reply_photo(photo=poster_path, caption=card_text,
                                      parse_mode='HTML', reply_markup=card_inline)
        else:
            await message.reply(card_text, parse_mode='HTML', reply_markup=card_inline)
    except Exception as e:
        await message.reply("Внутренняя ошибка. Уже исправляем.")
        print(e)
