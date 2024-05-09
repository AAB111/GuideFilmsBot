from aiogram.fsm.state import StatesGroup, State


class CardState(StatesGroup):
    inputTitle = State()


class ReviewState(StatesGroup):
    inputTitle = State()
    inputTypeReview = State()
    inputReview = State()


