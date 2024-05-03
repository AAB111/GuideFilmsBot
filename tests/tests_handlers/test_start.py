import pytest
from unittest import mock
from main import start
from unittest.mock import AsyncMock, patch
from tests.utils import TEST_USER


@pytest.mark.asyncio
async def test_start_handler_not_backend():
    with patch('main.request_auth', return_value=None) as mock_request_auth:
        message_mock = AsyncMock()
        message_mock.from_user.id = TEST_USER.id
        message_mock.from_user.full_name = TEST_USER.first_name + " " + TEST_USER.last_name
        await start(message_mock)

        assert mock_request_auth.call_count == 1
        assert mock_request_auth.call_args == mock.call(TEST_USER.id)

        message_mock.answer.assert_awaited_once_with('Что-то пошло не так. Попробуйте /start позже.')


@pytest.mark.asyncio
async def test_start_handler():
    with patch('main.request_auth', return_value=200) as mock_request_auth:
        message_mock = AsyncMock()
        message_mock.from_user.id = TEST_USER.id
        message_mock.from_user.full_name = TEST_USER.first_name + " " + TEST_USER.last_name
        await start(message_mock)
        assert mock_request_auth.call_count == 1
        assert mock_request_auth.call_args == mock.call(TEST_USER.id)
        expected_welcome_text = (
            f"Привет, {message_mock.from_user.full_name}! Добро пожаловать в мир фильмов! 🎬\n\n"
            "Я - ваш проводник в этом удивительном мире.\n"
            "Моя задача - помочь вам найти лучшие фильмы для просмотра и наслаждения.\n"
            "Спросите меня о популярных фильмах или составьте свой фильм.\n"
            "Если у вас есть описание фильма, который вы ищете, просто дайте мне знать, и я найду для вас похожие фильмы!\n"
            "И помните, я всегда здесь, чтобы помочь вам в выборе фильма для вашего вечера! 🍿"
            "Доступные команды:\n"
            "/card - получить информацию о конкретном фильме\n"
        )
        message_mock.answer.assert_awaited_once_with(expected_welcome_text)
