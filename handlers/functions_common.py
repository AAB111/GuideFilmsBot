
async def show_group_movies(movies, send_message, top_n=10):
    media = []
    top_5_message = "<b>Посмотри что нашёл</b>\n\n"
    for movie in movies[:top_n]:
        try:
            post_url = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
            title = movie['title']
            overview = movie['overview']
            post_text = f"{title}:\n{overview}\n"
            top_5_message += f"<b>{title}</b>:\n{overview}\n\n"
            media.append(movies.InputMediaPhoto(media=post_url, caption=post_text))
        except TimeoutError as e:
            pass
    if len(media) > 3:
        await send_message.reply_media_group(media=media, post_text="Посмотри что нашёл")
    else:
        await send_message.edit_text(top_5_message, parse_mode="HTML")