from aiogram.types import InputMediaPhoto


async def show_group_movies(movies):
    media = []
    for movie in movies:
        if movie['poster_path'] is not None:
            post_url = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
            title = movie['title']
            overview = movie['overview']
            post_text = f"{title}:\n{overview}\n"
            media.append(InputMediaPhoto(media=post_url, caption=post_text))
    return media


async def show_text_movies(movies):
    top_5_message = "<b>Посмотри что нашёл</b>\n\n"
    for movie in movies:
        top_5_message += f"<b>{movie['title']}</b>:\n{movie['overview']}\n\n"
    return top_5_message
