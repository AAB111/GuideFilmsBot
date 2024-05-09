from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class InfoRating(CallbackData, prefix='rating'):
    rating: int
    movie_id: int


class InfoAction(CallbackData, prefix='action'):
    movie_id: int
    action: str


class InfoTransition(CallbackData, prefix='transition'):
    movie_id: int


class TypeReview(CallbackData, prefix='type_review'):
    type_review: str


builder = InlineKeyboardBuilder()
builder.button(text='Положительный', callback_data=TypeReview(type_review='Положительный'))
builder.button(text='Нейтральный', callback_data=TypeReview(type_review='Нейтральный'))
builder.button(text='Отрицательный', callback_data=TypeReview(type_review='Отрицательный'))
type_review_keyboard = builder.as_markup(resize_keyboard=True)


def create_eval_inline(movie_id):
    builed_keyboard = InlineKeyboardBuilder()
    for i in range(10, 0, -1):
        builed_keyboard.button(text=f"{i} ⭐️", callback_data=InfoRating(rating=i, movie_id=movie_id))
    builed_keyboard.button(text="Назад", callback_data=InfoAction(action="back", movie_id=movie_id))
    builed_keyboard.adjust(*(1, 3, 3, 3, 1))
    return builed_keyboard.as_markup(resize_keyboard=True)


def create_card_inline(movie_id):
    builder_keyboard = InlineKeyboardBuilder()
    builder_keyboard.button(text='Оценить ⭐️', callback_data=InfoAction(movie_id=movie_id, action="evaluat"))
    builder_keyboard.button(text='Оставить отзыв ✍️', callback_data=InfoAction(movie_id=movie_id, action="review"))
    builder_keyboard.button(text='Добавить в закладки 📌',
                            callback_data=InfoAction(movie_id=movie_id, action="be_watching"))
    builder_keyboard.button(text='Не нравится 👎', callback_data=InfoAction(movie_id=movie_id, action="dislike"))
    builder_keyboard.button(text='Смотрел уже 👁️', callback_data=InfoAction(movie_id=movie_id, action="watched"))
    builder_keyboard.button(text='Найти похожее 🔍', callback_data=InfoAction(movie_id=movie_id, action="similar"))
    builder_keyboard.adjust(*(2, 2, 1, 1))
    card_inline = builder_keyboard.as_markup(resize_keyboard=True)
    return card_inline


def create_transition_inline(movies):
    num_batches = len(movies) // 8 + (len(movies) % 8 > 0)
    list_keyboards = []
    for i in range(num_batches):
        builder_keyboard = InlineKeyboardBuilder()
        start_index = i * 8
        end_index = (i + 1) * 8
        for movie in movies[start_index:end_index]:
            builder_keyboard.button(text=movie['title'],
                                    callback_data=InfoTransition(movie_id=movie['id']))
        adjust_tuple = tuple([1] * len(movies))
        builder_keyboard.adjust(*adjust_tuple)
        list_keyboards.append(builder_keyboard.as_markup(resize_keyboard=True))
    return list_keyboards
