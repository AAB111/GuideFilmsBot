from datetime import datetime
from unittest import mock
from unittest.mock import AsyncMock
import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from tests.conftest import storage, bot
from tests.utils import TEST_USER, TEST_USER_CHAT
from states.statesFSM import ReviewState
from handlers.review import review_input_title, review_input_type_review, review_input_review


@pytest.mark.asyncio
async def test_review_input_title(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = "Пострясающе"
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )

        await review_input_title(message, state)

        assert await state.get_state() == ReviewState.inputTypeReview
        message.reply.assert_awaited_with("Как вы оцениваете фильм?", reply_markup=mock.ANY)


@pytest.mark.asyncio
async def test_review_input_type_review(storage, bot):
    call = AsyncMock()
    type_review = AsyncMock()
    type_review.type_review = "Положительный"
    call.from_user.id = TEST_USER.id
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )

        await review_input_type_review(call, type_review, state)

        call.message.answer.assert_awaited_with('Отлично! Теперь напишите свой отзыв.')
        assert await state.get_state() == ReviewState.inputReview
        call.message.edit_text.assert_awaited_with(type_review.type_review)


@pytest.mark.asyncio
async def test_review_input_review_post_200(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.update_data(user_id=TEST_USER.id, movie_id=500, title='Крутота', type_review='Положительный',
                                review='Хороший фильм, состоятельно рекомендую!')
        with mock.patch('handlers.review.add_movie_to_list', return_value=200):
            await review_input_review(message, state)

            message.reply.assert_awaited_with("Спасибо за отзыв!")
            assert await state.get_state() is None


@pytest.mark.asyncio
async def test_review_input_review_patch_200(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.text = 'Хороший фильм, состоятельно рекомендую!'
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        data_req = {
            'user_id': TEST_USER.id,
            'movie_id': 500,
            'title': 'Крутота',
            'type_review': 'Положительный',
            'review': message.text
        }
        await state.update_data(**data_req)
        with mock.patch('handlers.review.add_movie_to_list', return_value=400) as mock_add_movie_to_list:
            with mock.patch('handlers.review.patch_movie_from_list', return_value=200) as mock_patch_movie_from_list:
                await review_input_review(message, state)

                assert mock_add_movie_to_list.call_count == 1
                assert mock_add_movie_to_list.call_args == mock.call('review', data_req)
                assert mock_patch_movie_from_list.call_count == 1
                assert mock_patch_movie_from_list.call_args == mock.call('review', data_req)

                message.reply.assert_awaited_with('Спасибо за отзыв!')
                assert await state.get_state() is None


@pytest.mark.asyncio
async def test_review_input_review_patch_400(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.text = 'Хороший фильм, состоятельно рекомендую!'
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        data_req = {
            'user_id': TEST_USER.id,
            'movie_id': 500,
            'title': 'Крутота',
            'type_review': 'Положительный',
            'review': message.text
        }
        await state.update_data(**data_req)
        with mock.patch('handlers.review.add_movie_to_list', return_value=400) as mock_add_movie_to_list:
            with mock.patch('handlers.review.patch_movie_from_list', return_value=400) as mock_patch_movie_from_list:
                await review_input_review(message, state)

                assert mock_add_movie_to_list.call_count == 1
                assert mock_add_movie_to_list.call_args == mock.call('review', data_req)
                assert mock_patch_movie_from_list.call_count == 1
                assert mock_patch_movie_from_list.call_args == mock.call('review', data_req)

                message.reply.assert_awaited_with("Что-то пошло не так. Попробуйте позже.")
                assert await state.get_state() is None


@pytest.mark.asyncio
async def test_review_input_review_none(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.text = 'Хороший фильм, состоятельно рекомендую!'
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        data_req = {
            'user_id': TEST_USER.id,
            'movie_id': 500,
            'title': 'Крутота',
            'type_review': 'Положительный',
            'review': message.text
        }
        await state.update_data(**data_req)
        with mock.patch('handlers.review.add_movie_to_list', return_value=None) as mock_add_movie_to_list:
            await review_input_review(message, state)

            assert mock_add_movie_to_list.call_count == 1
            assert mock_add_movie_to_list.call_args == mock.call('review', data_req)

            message.reply.assert_awaited_with("Что-то пошло не так. Попробуйте позже.")
            assert await state.get_state() is None
