from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from api.requests import (add_movie_to_list, patch_movie_from_list)
from kbrds.keyboards import TypeReview
from kbrds.keyboards import type_review_keyboard
from states.statesFSM import ReviewState

review_router = Router()


@review_router.message(ReviewState.inputTitle)
async def review_input_title(message: types.Message, state: FSMContext):
    title = message.text
    await message.reply("Отлично!")
    await state.update_data(title=title)
    await state.set_state(ReviewState.inputTypeReview)
    await message.reply("Как вы оцениваете фильм?", reply_markup=type_review_keyboard)


@review_router.callback_query(TypeReview.filter())
async def review_input_type_review(call: types.CallbackQuery,
                                   callback_data: TypeReview,
                                   state: FSMContext):
    await state.update_data(type_review=callback_data.type_review)
    await state.set_state(ReviewState.inputReview)
    await call.message.edit_text(callback_data.type_review)
    await call.message.reply(callback_data.type_review)
    await call.message.answer("Отлично! Теперь напишите свой отзыв.")


@review_router.message(ReviewState.inputReview)
async def review_input_review(message: types.Message,
                              state: FSMContext):
    await state.update_data(review=message.text)
    data = await state.get_data()
    data_req = {'movie_id': data['movie_id'],
                'user_id': message.from_user.id,
                'title': data['title'],
                'type_review': data['type_review']
                }
    status_post_http = await add_movie_to_list("reviews", data_req)
    await state.clear()
    match status_post_http:
        case 200:
            await message.reply("Спасибо за отзыв!")
        case 400:
            data_req = {'movie_id': data['movie_id'],
                        'user_id': message.from_user.id,
                        'title': data['title'],
                        'type_review': data['type_review'],
                        'review': data['review']}
            status_patch_http = await patch_movie_from_list('reviews', data_req)
            match status_patch_http:
                case 200:
                    await message.reply("Спасибо за отзыв!")
        case _:
            await message.reply("Что-то пошло не так. Попробуйте позже.")
