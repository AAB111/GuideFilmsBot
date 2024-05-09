from unittest import mock
from unittest.mock import AsyncMock
import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from kbrds.keyboards import create_transition_inline
from states.statesFSM import CardState
from tests.conftest import storage, bot
from tests.utils import TEST_USER, TEST_USER_CHAT
from handlers.card import (start_card, get_card_input_title, send_movie_card)


@pytest.mark.asyncio
async def test_card_start(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
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
        await get_card_input_title(message, state)
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
        await get_card_input_title(message, state)

        message.reply.assert_awaited_with('К сожалению, ничего не найдено. Попробуйте заново.')
        assert await state.get_state() is None


@pytest.mark.asyncio
async def test_card_start_input_title_find_len_more_1(storage, bot):
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = "Терминатор"
    movies = [
        {
            "id": 447365,
            "title": "Стражи Галактики Том. 3",
            "tagline": "Еще раз с чувством.",
            "overview": "Питер Квилл, все еще не оправившийся от потери Гаморы, должен сплотить вокруг себя свою команду, чтобы защитить вселенную, а также защитить одного из своих. Миссия, которая, если ее не завершить успешно, вполне может привести к концу Стражей, какими мы их знаем.",
            "vote_average": 7.974999904632568,
            "release_date": "2023-05-03",
            "poster_path": "/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg",
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
        },
        {
            "id": 496450,
            "title": "Чудеса: Ледибаг и Кот Нуар, фильм",
            "tagline": "Судьба мира в их руках.",
            "overview": "После того, как хранитель волшебных драгоценностей превратил неуклюжую девочку и популярного мальчика в супергероев, они никогда не смогут раскрыть свои личности — даже друг другу.",
            "vote_average": 7.738999843597412,
            "release_date": "2023-07-05",
            "poster_path": "/dQNJ8SdCMn3zWwHzzQD2xrphR1X.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 16,
                        "name": " Анимация"
                    }
                },
                {
                    "genre": {
                        "id": 14,
                        "name": " Фантазия"
                    }
                },
                {
                    "genre": {
                        "id": 28,
                        "name": " Действие"
                    }
                },
                {
                    "genre": {
                        "id": 10749,
                        "name": " Романтика"
                    }
                },
                {
                    "genre": {
                        "id": 10751,
                        "name": " Семья"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 140008,
                        "name": "The Awakening Production"
                    }
                },
                {
                    "company": {
                        "id": 2902,
                        "name": "SND"
                    }
                },
                {
                    "company": {
                        "id": 200503,
                        "name": "Fantawild"
                    }
                },
                {
                    "company": {
                        "id": 82973,
                        "name": "Zag Animation Studios"
                    }
                },
                {
                    "company": {
                        "id": 220039,
                        "name": "ON Animation Studios"
                    }
                }
            ]
        },
        {
            "id": 507089,
            "title": "Пять Ночей С Фредди",
            "tagline": "Сможете ли вы пережить пять ночей?",
            "overview": "Недавно уволенный и отчаянно нуждающийся в работе, проблемный молодой человек по имени Майк соглашается устроиться на должность ночного охранника в заброшенном тематическом ресторане: пиццерия Фредди Фазбира. Но вскоре он обнаруживает, что во Фредди все не то, чем кажется.",
            "vote_average": 7.6570000648498535,
            "release_date": "2023-10-25",
            "poster_path": "/A4j8S6moJS2zNtRR8oWF08gRnL5.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 27,
                        "name": " Ужастик"
                    }
                },
                {
                    "genre": {
                        "id": 9648,
                        "name": " Тайна"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 3172,
                        "name": "Blumhouse Productions"
                    }
                },
                {
                    "company": {
                        "id": 211144,
                        "name": "Scott Cawthon Productions"
                    }
                }
            ]
        }
    ]
    with mock.patch('handlers.card.get_movies_by_title', return_value=movies):
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
            await get_card_input_title(message, state)
            message_text = "Я нашёл несколько подходящих фильмов."
            kbrds = create_transition_inline(movies)
            for kbrd in kbrds:
                await message.reply(message_text, reply_markup=kbrd)
            message.reply.assert_awaited_with(message_text, reply_markup=kbrds[-1])


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
        await get_card_input_title(message, state)

        message.reply.assert_awaited_with('К сожалению, ничего не найдено. Попробуйте заново.')
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
    result = {'status': 200, 'data': movie}
    await send_movie_card(message, result)
    message.reply.assert_not_awaited()
    message.reply_photo.assert_awaited()


@pytest.mark.asyncio
async def test_send_movie_card_movie_none():
    movie = {}
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    message.chat.id = TEST_USER_CHAT.id
    message.text = '2000'
    result = {'status': 200, 'data': movie}
    await send_movie_card(message, result)
    message.reply.assert_awaited_with('К сожалению, ничего не найдено. Попробуйте заново.')
    message.reply_photo.assert_not_awaited()
