from aiogram.fsm.state import StatesGroup, State


class CardState(StatesGroup):
    inputTitle = State()
    inputYear = State()
    selectMovie = State()


class ReviewState(StatesGroup):
    inputTitle = State()
    inputTypeReview = State()
    inputReview = State()

