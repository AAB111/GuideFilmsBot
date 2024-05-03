from handlers.be_watching import get_be_watching
from unittest import mock

import pytest
from unittest.mock import AsyncMock, patch
from handlers.functions_common import show_group_movies, show_text_movies
from tests.utils import TEST_USER, TEST_USER_NO_VALID

@pytest.mark.asyncio
async def test_get_be_watching_not_valid_user():
    message = AsyncMock()
    message.from_user.id = TEST_USER_NO_VALID.id
    await get_be_watching(message)
    message.reply.assert_awaited_with("Что-то пошло не так. Попробуйте /start снова.")


@pytest.mark.asyncio
async def test_get_be_watching_movies_len_0():
    message = AsyncMock()
    message.from_user.id = TEST_USER.id
    movies = []
    with patch('handlers.be_watching.get_movie_from_list', return_value=movies) as mock_get_be_watching:
        await get_be_watching(message)
        assert mock_get_be_watching.call_count == 1
        mock_get_be_watching.assert_awaited_with("be_watching", {"user_id": TEST_USER.id})
        message.reply.assert_awaited_with("В списке пусто.")


@pytest.mark.asyncio
async def test_get_be_watching_all_media():
    movies = [
        {
            "movie_id": 105,
            "datetime_added": "2024-04-29T12:17:40.577888",
            "movie": {
                "id": 105,
                "title": "Назад в будущее",
                "tagline": "Он никогда не приходил на занятия. Он не успел к ужину. И вот однажды... он вообще был не в своем времени.",
                "overview": "Подросток восьмидесятых годов Марти МакФлай случайно отправляется в прошлое, в 1955 год, что непреднамеренно срывает первую встречу его родителей и вызывает романтический интерес его матери. Марти должен исправить ущерб, нанесенный истории, возродив роман своих родителей и - с помощью своего эксцентричного друга-изобретателя Дока Брауна - вернуться в 1985 год.",
                "vote_average": 8.317000389099121,
                "release_date": "1985-07-03",
                "poster_path": "/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg",
                "genres": [
                    {
                        "genre": {
                            "id": 12,
                            "name": " Приключение"
                        }
                    },
                    {
                        "genre": {
                            "id": 35,
                            "name": " Комедия"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 33,
                            "name": "Universal Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 56,
                            "name": "Amblin Entertainment"
                        }
                    }
                ]
            }
        },
        {
            "movie_id": 280,
            "datetime_added": "2024-05-01T11:21:48.905831",
            "movie": {
                "id": 280,
                "title": "Терминатор 2: Судный день",
                "tagline": "Ничего личного.",
                "overview": "Действие классического научно-фантастического боевика Джеймса Кэмерона происходит через десять лет после событий оригинала. Он рассказывает историю второй попытки избавиться от лидера восстания Джона Коннора, на этот раз нацеленной на самого мальчика. Однако восстание послало перепрограммированного терминатора, чтобы защитить Коннора.",
                "vote_average": 8.111000061035156,
                "release_date": "1991-07-03",
                "poster_path": "/5M0j0B18abtBI5gi2RhfjjurTqb.jpg",
                "genres": [
                    {
                        "genre": {
                            "id": 28,
                            "name": " Действие"
                        }
                    },
                    {
                        "genre": {
                            "id": 53,
                            "name": " Триллер"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 275,
                            "name": "Carolco Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 1280,
                            "name": "Pacific Western"
                        }
                    },
                    {
                        "company": {
                            "id": 574,
                            "name": "Lightstorm Entertainment"
                        }
                    },
                    {
                        "company": {
                            "id": 183,
                            "name": "Le Studio Canal+"
                        }
                    },
                    {
                        "company": {
                            "id": 559,
                            "name": "TriStar Pictures"
                        }
                    }
                ]
            }
        },
        {
            "movie_id": 165,
            "datetime_added": "2024-05-01T11:21:50.891671",
            "movie": {
                "id": 165,
                "title": "Назад в будущее, часть 2.",
                "tagline": "Возвращение было только началом.",
                "overview": "Марти и Док снова в этом дурацком продолжении блокбастера 1985 года, где путешествующий во времени дуэт отправляется в 2015 год, чтобы пресечь некоторые семейные проблемы МакФлаев в зародыше. Но дела идут наперекосяк из-за хулигана Биффа Таннена и надоедливого спортивного альманаха. В последней попытке все исправить, Марти оказывается в 1955 году и снова оказывается лицом к лицу со своими родителями-подростками.",
                "vote_average": 7.760000228881836,
                "release_date": "1989-11-22",
                "poster_path": "/hQq8xZe5uLjFzSBt4LanNP7SQjl.jpg",
                "genres": [
                    {
                        "genre": {
                            "id": 12,
                            "name": " Приключение"
                        }
                    },
                    {
                        "genre": {
                            "id": 35,
                            "name": " Комедия"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 33,
                            "name": "Universal Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 56,
                            "name": "Amblin Entertainment"
                        }
                    }
                ]
            }
        },
        {
            "movie_id": 218,
            "datetime_added": "2024-05-01T11:21:56.720806",
            "movie": {
                "id": 218,
                "title": "Терминатор",
                "tagline": "Ваше будущее в его руках.",
                "overview": "В постапокалиптическом будущем правящие тиранические суперкомпьютеры телепортируют киборга-убийцу, известного как «Терминатор», обратно в 1984 год, чтобы убить Сару Коннор, чьему нерожденному сыну суждено возглавить повстанцев против механической гегемонии 21 века. Тем временем движение человеческого сопротивления отправляет одинокого воина защитить Сару. Сможет ли он остановить практически неразрушимую машину убийств?",
                "vote_average": 7.660999774932861,
                "release_date": "1984-10-26",
                "poster_path": "/qvktm0BHcnmDpul4Hz01GIazWPr.jpg",
                "genres": [
                    {
                        "genre": {
                            "id": 28,
                            "name": " Действие"
                        }
                    },
                    {
                        "genre": {
                            "id": 53,
                            "name": " Триллер"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 41,
                            "name": "Orion Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 3952,
                            "name": "Hemdale"
                        }
                    },
                    {
                        "company": {
                            "id": 1280,
                            "name": "Pacific Western"
                        }
                    },
                    {
                        "company": {
                            "id": 4764,
                            "name": "Cinema 84"
                        }
                    }
                ]
            }
        }
    ]
    with patch('handlers.be_watching.get_movie_from_list', return_value=movies) as mock_get_be_watching:
        message = AsyncMock()
        message.from_user.id = TEST_USER.id
        await get_be_watching(message)
        movies = [movie['movie'] for movie in movies]
        media = await show_group_movies(movies)
        assert mock_get_be_watching.call_count == 1
        assert mock_get_be_watching.call_args == mock.call("be_watching", {"user_id": TEST_USER.id})
        message.reply_media_group.assert_awaited_with(media=media)


@pytest.mark.asyncio
async def test_get_be_watching_media_and_not_poster():
    movies = [
        {
            "movie_id": 105,
            "datetime_added": "2024-04-29T12:17:40.577888",
            "movie": {
                "id": 105,
                "title": "Назад в будущее",
                "tagline": "Он никогда не приходил на занятия. Он не успел к ужину. И вот однажды... он вообще был не в своем времени.",
                "overview": "Подросток восьмидесятых годов Марти МакФлай случайно отправляется в прошлое, в 1955 год, что непреднамеренно срывает первую встречу его родителей и вызывает романтический интерес его матери. Марти должен исправить ущерб, нанесенный истории, возродив роман своих родителей и - с помощью своего эксцентричного друга-изобретателя Дока Брауна - вернуться в 1985 год.",
                "vote_average": 8.317000389099121,
                "release_date": "1985-07-03",
                "poster_path": "/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg",
                "genres": [
                    {
                        "genre": {
                            "id": 12,
                            "name": " Приключение"
                        }
                    },
                    {
                        "genre": {
                            "id": 35,
                            "name": " Комедия"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 33,
                            "name": "Universal Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 56,
                            "name": "Amblin Entertainment"
                        }
                    }
                ]
            }
        },
        {
            "movie_id": 280,
            "datetime_added": "2024-05-01T11:21:48.905831",
            "movie": {
                "id": 280,
                "title": "Терминатор 2: Судный день",
                "tagline": "Ничего личного.",
                "overview": "Действие классического научно-фантастического боевика Джеймса Кэмерона происходит через десять лет после событий оригинала. Он рассказывает историю второй попытки избавиться от лидера восстания Джона Коннора, на этот раз нацеленной на самого мальчика. Однако восстание послало перепрограммированного терминатора, чтобы защитить Коннора.",
                "vote_average": 8.111000061035156,
                "release_date": "1991-07-03",
                "poster_path": "/5M0j0B18abtBI5gi2RhfjjurTqb.jpg",
                "genres": [
                    {
                        "genre": {
                            "id": 28,
                            "name": " Действие"
                        }
                    },
                    {
                        "genre": {
                            "id": 53,
                            "name": " Триллер"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 275,
                            "name": "Carolco Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 1280,
                            "name": "Pacific Western"
                        }
                    },
                    {
                        "company": {
                            "id": 574,
                            "name": "Lightstorm Entertainment"
                        }
                    },
                    {
                        "company": {
                            "id": 183,
                            "name": "Le Studio Canal+"
                        }
                    },
                    {
                        "company": {
                            "id": 559,
                            "name": "TriStar Pictures"
                        }
                    }
                ]
            }
        },
        {
            "movie_id": 165,
            "datetime_added": "2024-05-01T11:21:50.891671",
            "movie": {
                "id": 165,
                "title": "Назад в будущее, часть 2.",
                "tagline": "Возвращение было только началом.",
                "overview": "Марти и Док снова в этом дурацком продолжении блокбастера 1985 года, где путешествующий во времени дуэт отправляется в 2015 год, чтобы пресечь некоторые семейные проблемы МакФлаев в зародыше. Но дела идут наперекосяк из-за хулигана Биффа Таннена и надоедливого спортивного альманаха. В последней попытке все исправить, Марти оказывается в 1955 году и снова оказывается лицом к лицу со своими родителями-подростками.",
                "vote_average": 7.760000228881836,
                "release_date": "1989-11-22",
                "poster_path": None,
                "genres": [
                    {
                        "genre": {
                            "id": 12,
                            "name": " Приключение"
                        }
                    },
                    {
                        "genre": {
                            "id": 35,
                            "name": " Комедия"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 33,
                            "name": "Universal Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 56,
                            "name": "Amblin Entertainment"
                        }
                    }
                ]
            }
        },
        {
            "movie_id": 218,
            "datetime_added": "2024-05-01T11:21:56.720806",
            "movie": {
                "id": 218,
                "title": "Терминатор",
                "tagline": "Ваше будущее в его руках.",
                "overview": "В постапокалиптическом будущем правящие тиранические суперкомпьютеры телепортируют киборга-убийцу, известного как «Терминатор», обратно в 1984 год, чтобы убить Сару Коннор, чьему нерожденному сыну суждено возглавить повстанцев против механической гегемонии 21 века. Тем временем движение человеческого сопротивления отправляет одинокого воина защитить Сару. Сможет ли он остановить практически неразрушимую машину убийств?",
                "vote_average": 7.660999774932861,
                "release_date": "1984-10-26",
                "poster_path": None,
                "genres": [
                    {
                        "genre": {
                            "id": 28,
                            "name": " Действие"
                        }
                    },
                    {
                        "genre": {
                            "id": 53,
                            "name": " Триллер"
                        }
                    },
                    {
                        "genre": {
                            "id": 878,
                            "name": " Научная фантастика"
                        }
                    }
                ],
                "companies": [
                    {
                        "company": {
                            "id": 41,
                            "name": "Orion Pictures"
                        }
                    },
                    {
                        "company": {
                            "id": 3952,
                            "name": "Hemdale"
                        }
                    },
                    {
                        "company": {
                            "id": 1280,
                            "name": "Pacific Western"
                        }
                    },
                    {
                        "company": {
                            "id": 4764,
                            "name": "Cinema 84"
                        }
                    }
                ]
            }
        }
    ]
    with patch('handlers.be_watching.get_movie_from_list', return_value=movies) as mock_get_be_watching:
        message = AsyncMock()
        message.from_user.id = TEST_USER.id
        await get_be_watching(message)

        assert mock_get_be_watching.call_count == 1
        assert mock_get_be_watching.call_args == mock.call("be_watching", {"user_id": TEST_USER.id})

        movies = [movie['movie'] for movie in movies]
        movies_poster_path_none = list(filter(lambda movie: movie['poster_path'] is None, movies))
        media = await show_group_movies(movies)
        text_reply = await show_text_movies(movies_poster_path_none)
        message.reply.assert_awaited_with(text_reply, parse_mode="HTML")
        message.reply_media_group.assert_awaited_with(media=media)
