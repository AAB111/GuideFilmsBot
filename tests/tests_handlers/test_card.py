from datetime import datetime
from unittest.mock import AsyncMock
import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from api.requests import get_movies_by_title
from states.statesFSM import CardState
from tests.conftest import storage, bot
from tests.utils import TEST_USER, TEST_USER_CHAT
from handlers.card import (start_card, get_card_input_title,
                           get_card_select_movie, get_card_input_year, send_movie_card)


@pytest.mark.asyncio
async def test_card_start(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    state = None
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await start_card(message, state)
        assert await state.get_state() == CardState.inputTitle
        message.reply.assert_awaited_with("Напишите название фильма")


@pytest.mark.asyncio
async def test_card_start_input_title_find_len_1(storage, bot):
    message = AsyncMock()
    message.text = "Терминатор 2"
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.update_data(chat_id=TEST_USER_CHAT.id,
                                send_message_id=50)
        await get_card_input_title(message, state, bot)
        assert await state.get_state() is None


@pytest.mark.asyncio
async def test_card_start_input_title_empty(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = ""
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.set_state(CardState.inputTitle)
        await state.update_data(chat_id=TEST_USER_CHAT.id, send_message_id=50)
        await get_card_input_title(message, state, bot)

        message.reply.assert_awaited_with('К сожалению, ничего не найдено. Попробуйте заново.')
        assert await state.get_state() is None


@pytest.mark.asyncio
async def test_card_start_input_title_find_len_more_1(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = "Терминатор"
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.set_state(CardState.inputTitle)
        await state.update_data(chat_id=TEST_USER_CHAT.id, send_message_id=50)
        await get_card_input_title(message, state, bot)
        searched_movies = await get_movies_by_title(message.text)
        message_text = "Я нашёл несколько подходящих фильмов. Введите <b>полное название</b>:\n\n"
        for movie in searched_movies:
            message_text += movie['title'] + f" ({datetime.strptime(movie['release_date'], '%Y-%m-%d').year})\n"

        message.reply.assert_awaited_with(message_text, parse_mode="HTML")
        assert await state.get_state() == CardState.selectMovie


@pytest.mark.asyncio
async def test_card_start_input_title_long(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasdfhgjhkfdsfdghfgjhgfdsadsfgnhfdsadfghfds")
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.set_state(CardState.inputTitle)
        await state.update_data(chat_id=TEST_USER_CHAT.id, send_message_id=50)
        await get_card_input_title(message, state, bot)

        message.reply.assert_awaited_with('К сожалению, ничего не найдено. Попробуйте заново.')
        assert await state.get_state() is None


@pytest.mark.asyncio
async def test_card_select_movie_len_1(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = "РобоКоп 2"
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        title = "РобоКоп"
        searched_movies = await get_movies_by_title(title)
        await state.update_data(searched_movies=searched_movies)
        await get_card_select_movie(message, state)
        assert await state.get_state() is None


@pytest.mark.asyncio
async def test_card_select_movie_title_no_valid(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = "adsfgh"
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        title = "РобоКоп"
        searched_movies = await get_movies_by_title(title)
        await state.update_data(searched_movies=searched_movies)

        await get_card_select_movie(message, state)

        message.reply.assert_awaited_with("Неправильное название. Попробуйте ещё раз")


@pytest.mark.asyncio
async def test_card_select_movie_len_more_1(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = "Робокоп"
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.set_state(CardState.selectMovie)
        title = "РобоКоп"
        searched_movies = await get_movies_by_title(title)
        await state.update_data(searched_movies=searched_movies)
        await get_card_select_movie(message, state)

        message.reply.assert_awaited_with("Нашёл несколко похожих фильмов. Введите <b>год</b> для уточнения:",
                                          parse_mode="HTML")
        assert await state.get_state() == CardState.inputYear
        assert (await state.get_data())['selecting_movies'] is not None


@pytest.mark.asyncio
async def test_card_input_year_no_valid(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = '2000'
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.set_state(CardState.inputYear)
        title = "РобоКоп"
        searched_movies = await get_movies_by_title(title)
        selected_movies = list(filter(lambda movie: title.strip().lower() == movie['title'].strip().lower(),
                                      searched_movies))
        await state.update_data(selecting_movies=selected_movies)
        await get_card_input_year(message, state)

        message.reply.assert_awaited_with("Что-то пошло не так. Попробуйте ещё раз")


@pytest.mark.asyncio
async def test_card_input_year_valid(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = '1987'
    async for stor in storage:
        state = FSMContext(
            storage=stor,
            key=StorageKey(
                bot_id=bot.id,
                user_id=TEST_USER.id,
                chat_id=TEST_USER_CHAT.id
            )
        )
        await state.set_state(CardState.inputYear)
        title = "РобоКоп"
        searched_movies = await get_movies_by_title(title)
        selected_movies = list(filter(lambda movie: title.strip().lower() == movie['title'].strip().lower(),
                                      searched_movies))
        await state.update_data(selecting_movies=selected_movies)
        await get_card_input_year(message, state)

        assert await state.get_state() is None

@pytest.mark.asyncio
async def test_send_movie_card_poster_none():
    movie = {
        "id": 447365,
        "title": "Стражи Галактики Том. 3",
        "tagline": "Еще раз с чувством.",
        "overview": "Питер Квилл, все еще не оправившийся от потери Гаморы, должен сплотить вокруг себя свою команду, "
                    "чтобы защитить вселенную, а также защитить одного из своих. Миссия, которая, если ее не "
                    "завершить успешно, вполне может привести к концу Стражей, какими мы их знаем.",
        "vote_average": 7.974999904632568,
        "release_date": "2023-05-03",
        "poster_path": None,
        "genres": [
            {
                "genre": {
                    "id": 878,
                    "name": " Научная фантастика"
                }
            },
            {
                "genre": {
                    "id": 12,
                    "name": " Приключение"
                }
            },
            {
                "genre": {
                    "id": 28,
                    "name": " Действие"
                }
            }
        ],
        "companies": [
            {
                "company": {
                    "id": 420,
                    "name": "Marvel Studios"
                }
            },
            {
                "company": {
                    "id": 176762,
                    "name": "Kevin Feige Productions"
                }
            }
        ]
    }
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = '2000'
    await send_movie_card(message, movie)
    message.reply_photo.assert_not_awaited()
    message.reply.assert_awaited()

@pytest.mark.asyncio
async def test_send_movie_card_poster_exists():
    movie = {
        "id": 447365,
        "title": "Стражи Галактики Том. 3",
        "tagline": "Еще раз с чувством.",
        "overview": "Питер Квилл, все еще не оправившийся от потери Гаморы, должен сплотить вокруг себя свою команду, "
                    "чтобы защитить вселенную, а также защитить одного из своих. Миссия, которая, если ее не "
                    "завершить успешно, вполне может привести к концу Стражей, какими мы их знаем.",
        "vote_average": 7.974999904632568,
        "release_date": "2023-05-03",
        "poster_path": "/asdheefg.jpg",
        "genres": [
            {
                "genre": {
                    "id": 878,
                    "name": " Научная фантастика"
                }
            },
            {
                "genre": {
                    "id": 12,
                    "name": " Приключение"
                }
            },
            {
                "genre": {
                    "id": 28,
                    "name": " Действие"
                }
            }
        ],
        "companies": [
            {
                "company": {
                    "id": 420,
                    "name": "Marvel Studios"
                }
            },
            {
                "company": {
                    "id": 176762,
                    "name": "Kevin Feige Productions"
                }
            }
        ]
    }
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = '2000'
    await send_movie_card(message, movie)
    message.reply.assert_not_awaited()
    message.reply_photo.assert_awaited()


@pytest.mark.asyncio
async def test_send_movie_card_movie_none():
    movie = None
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = '2000'
    await send_movie_card(message, movie)
    message.reply.assert_not_awaited()
    message.reply_photo.assert_not_awaited()