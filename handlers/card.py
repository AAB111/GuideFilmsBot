from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.statesFSM import CardState, ReviewState
from aiogram.filters import Command
from datetime import datetime
from api.requests import (get_movies_by_title, add_movie_to_list, patch_movie_from_list, delete_movie_from_list)
from kbrds.keyboards import cancel_inline, create_card_inline, create_eval_inline, InfoMovie, InfoRating, InfoAction
from aiogram import Bot

card_router = Router()


@card_router.message(Command('card'))
async def card_start(message: types.Message, state: FSMContext):
    send_message = await message.reply("Напишите название фильма", reply_markup=cancel_inline)
    await state.set_state(CardState.inputTitle)
    await state.update_data(send_message_id=send_message.message_id)
    await state.update_data(chat_id=message.chat.id)


@card_router.message(CardState.inputTitle)
async def get_card_input_title(message: types.Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        await bot.edit_message_reply_markup(data['chat_id'], data['send_message_id'], reply_markup=None)
        searched_movies = await get_movies_by_title(message.text)
        if searched_movies is not None:
            if len(searched_movies) > 1:
                await state.update_data(searched_movies=searched_movies)
                message_text = "Я нашёл несколько подходящих фильмов. Введите <b>полное название</b>:\n\n"
                for movie in searched_movies:
                    message_text += movie['title'] + f" ({datetime.strptime(movie['release_date'], '%Y-%m-%d').year})\n"
                await message.reply(message_text, parse_mode="HTML")
                await state.set_state(CardState.selectMovie)
                return
            elif len(searched_movies) == 1:
                first_element = searched_movies[0]
                await send_movie_card(message, first_element)
                await state.clear()
                return
        await message.reply("К сожалению, ничего не найдено. Попробуйте ввести название заново")
    except Exception as e:
        print(e)
        await message.reply("Произошла непредвиденная ошибка. Попробуйте ввести название заново")


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
    title = movie['title']
    overview = movie['overview']
    release_date = movie['release_date']
    poster_path = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"

    genres = ', '.join(genre['genre']['name'] for genre in movie['genres'])
    companies = ', '.join(company['company']['name'] for company in movie['companies'])

    card_text = f"<b>{title}</b>\n\n" \
                f"<i>Release Date:</i> {release_date}\n" \
                f"<i>Genres:</i> {genres}\n" \
                f"<i>Companies:</i> {companies}\n\n" \
                f"{overview}"
    card_inline = create_card_inline(movie['id'])
    try:
        await message.reply_photo(photo=poster_path, caption=card_text, parse_mode='HTML', reply_markup=card_inline)
    except Exception as e:
        await message.reply(card_text, parse_mode='HTML', reply_markup=card_inline)


@card_router.callback_query(F.data.contains('cancel'))
async def cancel_card(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text("Операция отменена")


@card_router.callback_query(InfoAction.filter())
async def cancel_card(call: types.CallbackQuery, callback_data: InfoAction, bot: Bot):
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
        data_req = {'movie_id': callback_data.movie_id,'user_id': callback.from_user.id}
        status_post_http = await add_movie_to_list('be_watching', data_req)
        match status_post_http:
            case 200:
                await callback.answer("Фильм добавлен в закладки")
            case 400:
                data_req = {'movie_id': callback_data.movie_id,
                            'user_id': callback.from_user.id}
                status_delete_http = await delete_movie_from_list('be_watching', data_req)
                match status_delete_http:
                    case 200:
                        await callback.answer("Фильм удален из закладок")
            case _:
                await callback.answer("Внутренная ошибка. Попробуйте ещё раз")
    elif callback_data.action == 'dislike':
        data_req = {'movie_id': callback_data.movie_id,
                    'user_id': callback.from_user.id}
        status_post_http = await add_movie_to_list('negative',
                                                   data_req)
        match status_post_http:
            case 200:
                await callback.answer("Постараюсь рекомендовать меньше похожего")
            case 400:
                data_req = {'movie_id': callback_data.movie_id,
                            'user_id': callback.from_user.id
                            }
                status_del = await delete_movie_from_list('negative', data_req)
                match status_del:
                    case 200:
                        await callback.answer('Фильм удален из "не нравится"')
            case _:
                await callback.answer("Внутренная ошибка. Попробуйте ещё раз")
    elif callback_data.action == 'review':
        await callback.message.answer("Напишите заголовок отзыва")
        await state.set_state(ReviewState.inputTitle)
        await state.update_data(movie_id=callback_data.movie_id)
    elif callback_data.action == 'watched':
        data_req = {'movie_id': callback_data.movie_id,
                    'user_id': callback.from_user.id}
        status_post_http = await add_movie_to_list('watched', data_req)
        if status_post_http in [200, 400]:
            await callback.answer("Поделитесь своим мнением об этом фильме. Я буду рад услышать ваш отзыв!")
        else:
            print('Внутренная ошибка. Попробуйте ещё раз')


@card_router.callback_query(InfoRating.filter())
async def handle_callback_eval(callback: types.CallbackQuery, callback_data: InfoRating):
    data_req = {'user_id': callback.from_user.id,
                'movie_id': callback_data.movie_id,
                'rating': callback_data.rating}
    status_post_http = await add_movie_to_list('evaluated', data_req)
    match status_post_http:
        case 200:
            await callback.answer("Спасибо за оценку!")
        case 400:
            data_req = {'user_id': callback.from_user.id,
                        'movie_id': callback_data.movie_id,
                        'rating': callback_data.rating
                        }
            status_patch_http = await patch_movie_from_list('evaluated', data_req)
            match status_patch_http:
                case 200:
                    await callback.answer("Спасибо за оценку!")
        case _:
            await callback.answer("Внутренная ошибка. Попробуйте ещё раз.")
