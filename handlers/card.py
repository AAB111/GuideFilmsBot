from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from handlers.functions_common import send_movie_card, show_group_movies_message
from states.statesFSM import CardState, ReviewState
from aiogram.filters import Command
from api.requests import (get_movies_by_title, add_movie_to_list, patch_movie_from_list, delete_movie_from_list,
                          get_similar_movies)
from kbrds.keyboards import (create_card_inline, create_eval_inline, InfoRating,
                             InfoAction, create_transition_inline)
from aiogram import Bot

card_router = Router()


@card_router.message(Command('card'))
async def start_card(message: types.Message, state: FSMContext):
    await message.reply("Напишите название фильма")
    await state.set_state(CardState.inputTitle)


@card_router.message(CardState.inputTitle)
async def get_card_input_title(message: types.Message, state: FSMContext):
    try:
        result = await get_movies_by_title(message.text)
        await state.clear()
        if result['status'] != 200:
            await message.reply("К сожалению, ничего не найдено. Попробуйте заново.")
            return
        searched_movies = result['data']
        if len(searched_movies) > 1:
            message_text = "Я нашёл несколько подходящих фильмов."
            kbrds = create_transition_inline(searched_movies)
            for kbrd in kbrds:
                await message.reply(message_text, reply_markup=kbrd)
        elif len(searched_movies) == 1:
            first_element = searched_movies[0]
            print(first_element)
            await send_movie_card(message, first_element)
        return
    except Exception as e:
        print(e)
        await message.reply("Произошла непредвиденная ошибка")
        await state.clear()


@card_router.callback_query(InfoAction.filter())
async def handle_callback_query(callback: types.CallbackQuery, callback_data: InfoAction, bot: Bot, state: FSMContext):
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
    elif callback_data.action == 'similar':
        similar_movies = await get_similar_movies(callback_data.movie_id)
        await show_group_movies_message(callback.message, similar_movies, "Посмотрите похожие фильмы!")

    elif callback_data.action == 'back':
        card_inline = create_card_inline(callback_data.movie_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=card_inline)


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
