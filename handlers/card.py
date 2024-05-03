from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.statesFSM import CardState, ReviewState
from aiogram.filters import Command
from datetime import datetime
from api.requests import (get_movies_by_title, add_movie_to_list, patch_movie_from_list, delete_movie_from_list,
                          get_credits_by_id)
from kbrds.keyboards import (create_card_inline, create_eval_inline, InfoMovie, InfoRating,
                             InfoAction)
from aiogram import Bot

card_router = Router()


@card_router.message(Command('card'))
async def start_card(message: types.Message, state: FSMContext):
    send_message = await message.reply("Напишите название фильма")
    await state.set_state(CardState.inputTitle)


@card_router.message(CardState.inputTitle)
async def get_card_input_title(message: types.Message, state: FSMContext, bot: Bot):
    try:
        searched_movies = await get_movies_by_title(message.text)
        if searched_movies is not None:
            if len(searched_movies) > 1:
                await state.update_data(searched_movies=searched_movies)
                message_text = "Я нашёл несколько подходящих фильмов. Введите <b>полное название</b>:\n\n"
                for movie in searched_movies:
                    message_text += movie['title'] + f" ({datetime.strptime(movie['release_date'], '%Y-%m-%d').year})\n"
                await message.reply(message_text, parse_mode="HTML")
                await state.set_state(CardState.selectMovie)
            elif len(searched_movies) == 1:
                first_element = searched_movies[0]
                await send_movie_card(message, first_element)
                await state.clear()
            return
        await message.reply("К сожалению, ничего не найдено. Попробуйте заново.")
        await state.clear()
    except Exception as e:
        print(e)
        await message.reply("Произошла непредвиденная ошибка")
        await state.clear()


@card_router.message(CardState.selectMovie)
async def get_card_select_movie(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_movies = list(filter(lambda movie: message.text.strip().lower() == movie['title'].strip().lower(),
                                  data['searched_movies']))

    if len(selected_movies) == 1:
        first_element = selected_movies[0]
        await send_movie_card(message, first_element)
        await state.clear()
        return
    elif len(selected_movies) > 1:
        await state.update_data(selecting_movies=selected_movies)
        await state.set_state(CardState.inputYear)
        await message.reply("Нашёл несколко похожих фильмов. Введите <b>год</b> для уточнения:", parse_mode="HTML")
        return
    await message.reply("Неправильное название. Попробуйте ещё раз")


@card_router.message(CardState.inputYear)
async def get_card_input_year(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_movie = list(
        filter(lambda movie: datetime.strptime(movie['release_date'], '%Y-%m-%d').year == int(message.text),
               data['selecting_movies']))
    if len(selected_movie) == 1:
        first_element = selected_movie[0]
        await send_movie_card(message, first_element)
        await state.clear()
        return
    await message.reply("Что-то пошло не так. Попробуйте ещё раз")


async def send_movie_card(message: types.Message, movie: dict):
    try:
        title = movie['title']
        overview = movie['overview']
        release_date = movie['release_date']
        poster_path = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"

        genres = ', '.join(genre['genre']['name'] for genre in movie['genres'])
        companies = ', '.join(company['company']['name'] for company in movie['companies'])

        credits = await get_credits_by_id(movie['id'])
        if credits is not None:
            directors = [crew_member['person']['name'] for crew_member in credits[0]['crew'] if
                         crew_member['job'] == 'Режиссер']
            top_cast = sorted(credits[0]['cast'], key=lambda x: x['person']['popularity'], reverse=True)[:6]
            actors = [cast_member['person']['name'] for cast_member in top_cast]

            directors_text = ", ".join(directors)
            actors_text = ", ".join(actors)
            card_text = f"<b>{title}</b>\n\n" \
                        f"<i>Дата выхода:</i> {release_date}\n" \
                        f"<i>Жанры:</i> {genres}\n" \
                        f"<i>Компании:</i> {companies}\n\n" \
                        f"<i>Режиссер(ы):</i> {directors_text}\n\n" \
                        f"<i>В главных ролях:</i> {actors_text}\n\n" \
                        f"{overview}"
        else:
            card_text = f"<b>{title}</b>\n\n" \
                        f"<i>Дата выхода:</i> {release_date}\n" \
                        f"<i>Жанры:</i> {genres}\n" \
                        f"<i>Компании:</i> {companies}\n\n" \
                        f"{overview}"

        card_inline = create_card_inline(movie['id'])
        if movie['poster_path'] is not None:
            await message.reply_photo(photo=poster_path, caption=card_text, parse_mode='HTML', reply_markup=card_inline)
        else:
            await message.reply(card_text, parse_mode='HTML', reply_markup=card_inline)
    except Exception as e:
        print(e)


@card_router.callback_query(InfoAction.filter())
async def back_button_card(call: types.CallbackQuery, callback_data: InfoAction, bot: Bot):
    if callback_data.action == 'back':
        card_inline = create_card_inline(callback_data.movie_id)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=card_inline)


@card_router.callback_query(InfoMovie.filter())
async def handle_callback_query(callback: types.CallbackQuery, callback_data: InfoMovie, bot: Bot, state: FSMContext):
    if callback_data.action == 'evaluat':
        eval_kb = create_eval_inline(callback_data.movie_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=eval_kb)
    elif callback_data.action == 'be_watching':
        data_req = {'movie_id': callback_data.movie_id, 'user_id': callback.from_user.id}
        await handle_movie_list_callback(callback, 'Фильм добавлен в закладки', 'Фильм удален из закладок',
                                         'be_watching', add_movie_to_list, delete_movie_from_list, data_req)
    elif callback_data.action == 'dislike':
        data_req = {'movie_id': callback_data.movie_id,
                    'user_id': callback.from_user.id}
        await handle_movie_list_callback(callback, "Постараюсь рекомендовать меньше похожего",
                                         'Фильм удален из "не нравится"',
                                         'negative', add_movie_to_list, delete_movie_from_list, data_req)
    elif callback_data.action == 'review':
        await callback.message.answer("Напишите заголовок отзыва")
        await state.set_state(ReviewState.inputTitle)
        await state.update_data(movie_id=callback_data.movie_id)
    elif callback_data.action == 'watched':
        data_req = {'movie_id': callback_data.movie_id,
                    'user_id': callback.from_user.id}
        await handle_movie_list_callback(callback, "Поделитесь своим мнением об этом фильме. Я буду рад услышать ваш "
                                                   "отзыв!",
                                         "Жалко, что вы не посмотрели этот фильм.",
                                         'watched', add_movie_to_list, delete_movie_from_list, data_req)


@card_router.callback_query(InfoRating.filter())
async def handle_callback_eval(callback: types.CallbackQuery, callback_data: InfoRating):
    data_req = {'user_id': callback.from_user.id,
                'movie_id': callback_data.movie_id,
                'rating': callback_data.rating}
    await handle_movie_list_callback(callback, "Спасибо за оценку!", "Спасибо за оценку!",
                                     "evaluated", add_movie_to_list, patch_movie_from_list, data_req)


async def handle_movie_list_callback(callback: types.CallbackQuery, first_answer: str, second_answer: str,
                                     name_list: str,
                                     func_first,
                                     func_second, data_req: dict):
    status_http = await func_first(name_list, data_req)
    match status_http:
        case 200:
            await callback.answer(first_answer)
        case 400:
            status_http = await func_second(name_list, data_req)
            match status_http:
                case 200:
                    await callback.answer(second_answer)
                case _:
                    await callback.answer("Что-то пошло не так. Попробуйте позже.")
        case _:
            await callback.answer("Что-то пошло не так. Попробуйте позже.")
