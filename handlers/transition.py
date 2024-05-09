from aiogram import Router, types

from api.requests import get_movie_by_id
from handlers.functions_common import send_movie_card
from kbrds.keyboards import InfoTransition

transition_router = Router()


@transition_router.callback_query(InfoTransition.filter())
async def handle_callback_transition_movie(callback: types.CallbackQuery, callback_data: InfoTransition):
    result = await get_movie_by_id(callback_data.movie_id)
    await send_movie_card(callback.message, result)
