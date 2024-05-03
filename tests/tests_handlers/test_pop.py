from unittest import mock
from unittest.mock import AsyncMock
import pytest

from handlers.pop import start_pop
from handlers.functions_common import show_group_movies, show_text_movies


@pytest.mark.asyncio
async def test_pop_movies_is_none():
    with mock.patch('handlers.pop.get_pop_based',
                    return_value=None) as mock_get_pop_based:
        message = AsyncMock()
        await start_pop(message)
        assert mock_get_pop_based.call_count == 1
        assert mock_get_pop_based.call_args == mock.call()
        message.reply.assert_awaited_with('Внутренняя ошибка. Уже исправляем.')


@pytest.mark.asyncio
async def test_pop_movies_is_len_0():
    with mock.patch('handlers.pop.get_pop_based',
                    return_value=[]) as mock_get_pop_based:
        message = AsyncMock()
        await start_pop(message)
        assert mock_get_pop_based.call_count == 1
        assert mock_get_pop_based.call_args == mock.call()
        message.reply.assert_awaited_with('К сожалению, ничего не найдено.')


@pytest.mark.asyncio
async def test_pop_movies_poster_path_none():
    movies = [{
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
    }]

    with mock.patch('handlers.pop.get_pop_based', return_value=movies) as mock_get_pop_based:
        message = AsyncMock()
        await start_pop(message)

        assert mock_get_pop_based.call_count == 1
        assert mock_get_pop_based.call_args == mock.call()
        text_reply = await show_text_movies(movies)
        message.reply.assert_awaited_with(text_reply,
                                          parse_mode='HTML')


@pytest.mark.asyncio
async def test_pop_all_media():
    movies = [{
        "id": 447365,
        "title": "Стражи Галактики Том. 3",
        "tagline": "Еще раз с чувством.",
        "overview": "Питер Квилл, все еще не оправившийся от потери Гаморы, должен сплотить вокруг себя свою команду, "
                    "чтобы защитить вселенную, а также защитить одного из своих. Миссия, которая, если ее не "
                    "завершить успешно, вполне может привести к концу Стражей, какими мы их знаем.",
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
    }]
    with mock.patch('handlers.pop.get_pop_based', return_value=movies) as mock_get_pop_based:
        message = AsyncMock()
        await start_pop(message)

        assert mock_get_pop_based.call_count == 1
        assert mock_get_pop_based.call_args == mock.call()

        media = await show_group_movies(movies)
        message.reply_media_group.assert_awaited_with(media=media)


@pytest.mark.asyncio
async def test_pop_media_and_none_poster():
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
        },
        {
            "id": 569094,
            "title": "Человек-паук: Через вселенные",
            "tagline": "Важно то, как вы носите маску.",
            "overview": "После воссоединения с Гвен Стейси постоянный, дружелюбный Человек-Паук из Бруклина катапультируется через Мультивселенную, где он встречает Общество Пауков, команду Людей-Пауков, которой поручено защищать само существование Мультивселенной. Но когда герои спорят о том, как справиться с новой угрозой, Майлз сталкивается с другими пауками и должен отправиться в одиночку, чтобы спасти тех, кого он любит больше всего.",
            "vote_average": 8.399999618530273,
            "release_date": "2023-05-31",
            "poster_path": "/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 16,
                        "name": " Анимация"
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
                        "id": 12,
                        "name": " Приключение"
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
                        "id": 5,
                        "name": "Columbia Pictures"
                    }
                },
                {
                    "company": {
                        "id": 2251,
                        "name": "Sony Pictures Animation"
                    }
                },
                {
                    "company": {
                        "id": 77973,
                        "name": "Lord Miller"
                    }
                },
                {
                    "company": {
                        "id": 84041,
                        "name": "Pascal Pictures"
                    }
                },
                {
                    "company": {
                        "id": 14439,
                        "name": "Arad Productions"
                    }
                },
                {
                    "company": {
                        "id": 7505,
                        "name": "Marvel Entertainment"
                    }
                }
            ]
        },
        {
            "id": 575264,
            "title": "Миссия невыполнима: Мертвая расплата, часть первая",
            "tagline": "Мы все разделяем одну и ту же судьбу.",
            "overview": "Итан Хант и его команда из МВФ приступают к своей самой опасной миссии: выследить новое ужасающее оружие, которое угрожает всему человечеству, прежде чем оно попадет в чужие руки. Когда на кону стоит контроль над будущим и судьбой мира, а темные силы из прошлого Итана приближаются, начинается смертельная гонка по всему миру. Столкнувшись с загадочным и всемогущим врагом, Итан должен осознать, что ничто не может иметь большего значения, чем его миссия, даже жизни тех, о ком он заботится больше всего.",
            "vote_average": 7.554999828338623,
            "release_date": "2023-07-08",
            "poster_path": "/NNxYkU70HPurnNCSiCjYAmacwm.jpg",
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
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 4,
                        "name": "Paramount"
                    }
                },
                {
                    "company": {
                        "id": 82819,
                        "name": "Skydance Media"
                    }
                },
                {
                    "company": {
                        "id": 21777,
                        "name": "TC Productions"
                    }
                }
            ]
        },
        {
            "id": 666277,
            "title": "Прошлые жизни",
            "tagline": None,
            "overview": "Нора и Хэ Сон, двое друзей детства, воссоединяются в Нью-Йорке на одну судьбоносную неделю, когда они сталкиваются с понятиями судьбы, любви и выбора, который составляет жизнь.",
            "vote_average": 7.793000221252441,
            "release_date": "2023-06-02",
            "poster_path": "/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                },
                {
                    "genre": {
                        "id": 10749,
                        "name": " Романтика"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 41077,
                        "name": "A24"
                    }
                },
                {
                    "company": {
                        "id": 1422,
                        "name": "Killer Films"
                    }
                },
                {
                    "company": {
                        "id": 158407,
                        "name": "2AM"
                    }
                },
                {
                    "company": {
                        "id": 128404,
                        "name": "CJ ENM"
                    }
                }
            ]
        },
        {
            "id": 667538,
            "title": "Трансформеры: Восстание зверей",
            "tagline": "Объединитесь или падите.",
            "overview": "Когда появляется новая угроза, способная уничтожить всю планету, Оптимус Прайм и автоботы должны объединиться с могущественной фракцией, известной как Максималы. Поскольку судьба человечества висит на волоске, люди Ной и Елена сделают все возможное, чтобы помочь Трансформерам в решающей битве за спасение Земли.",
            "vote_average": 7.34499979019165,
            "release_date": "2023-06-06",
            "poster_path": "/gPbM0MK8CP8A174rmUwGsADNYKD.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 28,
                        "name": " Действие"
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
                        "id": 878,
                        "name": " Научная фантастика"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 82819,
                        "name": "Skydance Media"
                    }
                },
                {
                    "company": {
                        "id": 4,
                        "name": "Paramount"
                    }
                },
                {
                    "company": {
                        "id": 435,
                        "name": "di Bonaventura Pictures"
                    }
                },
                {
                    "company": {
                        "id": 6734,
                        "name": "Bay Films"
                    }
                },
                {
                    "company": {
                        "id": 114732,
                        "name": "New Republic Pictures"
                    }
                },
                {
                    "company": {
                        "id": 38831,
                        "name": "DeSanto/Murphy Productions"
                    }
                },
                {
                    "company": {
                        "id": 2598,
                        "name": "Hasbro"
                    }
                }
            ]
        },
        {
            "id": 678512,
            "title": "Звук свободы",
            "tagline": "Борьба за свет. Заставьте тьму замолчать.",
            "overview": "История Тима Балларда, бывшего правительственного агента США, который бросает работу, чтобы посвятить свою жизнь спасению детей от глобальных секс-торговцев.",
            "vote_average": 8.038999557495117,
            "release_date": "2023-07-03",
            "poster_path": "/qA5kPYZA7FkVvqcEfJRoOy4kpHg.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 28,
                        "name": " Действие"
                    }
                },
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 90508,
                        "name": "Santa Fe Films"
                    }
                }
            ]
        },
        {
            "id": 697843,
            "title": "Экстракция 2",
            "tagline": "Приготовьтесь к поездке всей вашей жизни.",
            "overview": "Получив задание спасти семью, оказавшуюся во власти грузинского гангстера, Тайлер Рэйк проникает в одну из самых смертоносных тюрем мира, чтобы спасти их. Но когда добыча становится жаркой, и гангстер погибает в пылу боя, его столь же безжалостный брат выслеживает Рейка и его команду в Вену, чтобы отомстить.",
            "vote_average": 7.46999979019165,
            "release_date": "2023-06-09",
            "poster_path": "/7gKI9hpEMcZUQpNgKrkDzJpbnNS.jpg",
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
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 106544,
                        "name": "AGBO"
                    }
                },
                {
                    "company": {
                        "id": 104576,
                        "name": "Filmhaus Films"
                    }
                }
            ]
        },
        {
            "id": 792307,
            "title": "Бедняжки",
            "tagline": "Она не похожа ни на что, что вы когда-либо видели.",
            "overview": "Возвращенная к жизни неортодоксальным ученым, молодая женщина убегает с развратным адвокатом в головокружительное приключение через континенты. Свободная от предрассудков своего времени, она становится твердой в своем стремлении отстаивать равенство и освобождение.",
            "vote_average": 7.818999767303467,
            "release_date": "2023-12-07",
            "poster_path": "/kCGlIMHnOm8JPXq3rXM6c5wMxcT.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 878,
                        "name": " Научная фантастика"
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
                        "id": 35,
                        "name": " Комедия"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 127929,
                        "name": "Searchlight Pictures"
                    }
                },
                {
                    "company": {
                        "id": 6705,
                        "name": "Film4 Productions"
                    }
                },
                {
                    "company": {
                        "id": 22213,
                        "name": "TSG Entertainment"
                    }
                },
                {
                    "company": {
                        "id": 3353,
                        "name": "Element Pictures"
                    }
                }
            ]
        },
        {
            "id": 840430,
            "title": "Остатки",
            "tagline": "Дискомфорт и радость.",
            "overview": "Ворчливый инструктор подготовительной школы Новой Англии вынужден оставаться в кампусе во время рождественских каникул, чтобы присматривать за горсткой учеников, которым некуда идти. В конце концов, у него возникает маловероятная связь с одним из них — ущербным и умным нарушителем спокойствия — и с главным поваром школы, который только что потерял сына во Вьетнаме.",
            "vote_average": 7.739999771118164,
            "release_date": "2023-10-27",
            "poster_path": "/VHSzNBTwxV8vh7wylo7O9CLdac.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 35,
                        "name": " Комедия"
                    }
                },
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 14,
                        "name": "Miramax"
                    }
                },
                {
                    "company": {
                        "id": 2605,
                        "name": "Gran Via Productions"
                    }
                }
            ]
        },
        {
            "id": 872585,
            "title": "Оппенгеймер",
            "tagline": "Мир навсегда меняется.",
            "overview": "Рассказ о роли Дж. Роберта Оппенгеймера в разработке атомной бомбы во время Второй мировой войны.",
            "vote_average": 8.112000465393066,
            "release_date": "2023-07-19",
            "poster_path": "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                },
                {
                    "genre": {
                        "id": 36,
                        "name": " История"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 9996,
                        "name": "Syncopy"
                    }
                },
                {
                    "company": {
                        "id": 33,
                        "name": "Universal Pictures"
                    }
                },
                {
                    "company": {
                        "id": 507,
                        "name": "Atlas Entertainment"
                    }
                }
            ]
        },
        {
            "id": 906126,
            "title": "Общество снега",
            "tagline": "Основано на замечательной реальной истории.",
            "overview": "13 октября 1972 года рейс 571 ВВС Уругвая, зафрахтованный для перевозки команды по регби в Чили, врезался в ледник в самом сердце Анд.",
            "vote_average": 8.065999984741211,
            "release_date": "2023-12-15",
            "poster_path": "/2e853FDVSIso600RqAMunPxiZjq.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                },
                {
                    "genre": {
                        "id": 36,
                        "name": " История"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 207052,
                        "name": "El Arriero Films"
                    }
                },
                {
                    "company": {
                        "id": 217668,
                        "name": "Misión de Audaces Films"
                    }
                },
                {
                    "company": {
                        "id": 178464,
                        "name": "Netflix"
                    }
                }
            ]
        },
        {
            "id": 915935,
            "title": "Анатомия падения",
            "tagline": "Она это сделала?",
            "overview": "Женщину подозревают в убийстве мужа, а их слепой сын оказывается перед моральной дилеммой, будучи единственным свидетелем.",
            "vote_average": 7.638999938964844,
            "release_date": "2023-08-23",
            "poster_path": "/kQs6keheMwCxJxrzV83VUwFtHkB.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 53,
                        "name": " Триллер"
                    }
                },
                {
                    "genre": {
                        "id": 9648,
                        "name": " Тайна"
                    }
                },
                {
                    "genre": {
                        "id": 80,
                        "name": " Преступление"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 58568,
                        "name": "Les Films de Pierre"
                    }
                },
                {
                    "company": {
                        "id": 12389,
                        "name": "Les Films Pelléas"
                    }
                },
                {
                    "company": {
                        "id": 83,
                        "name": "France 2 Cinéma"
                    }
                },
                {
                    "company": {
                        "id": 109756,
                        "name": "Auvergne-Rhône-Alpes Cinéma"
                    }
                }
            ]
        },
        {
            "id": 930094,
            "title": "Красный, белый и королевский синий",
            "tagline": "Люби того, кого хочешь. Это хорошая внешняя политика.",
            "overview": "После того, как ссора между Алексом, сыном президента, и британским принцем Генри на королевском мероприятии стала пищей для таблоидов, их давняя вражда теперь грозит вбить клин в американо-британские отношения. Когда соперники вынуждены заключить инсценированное перемирие, их ледяные отношения начинают таять, и трения между ними разжигают нечто более глубокое, чем они когда-либо ожидали.",
            "vote_average": 8.038000106811523,
            "release_date": "2023-07-27",
            "poster_path": "/dD3vhyDRCCT90hf4rldHU6Wu3Va.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 35,
                        "name": " Комедия"
                    }
                },
                {
                    "genre": {
                        "id": 10749,
                        "name": " Романтика"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 20580,
                        "name": "Amazon Studios"
                    }
                },
                {
                    "company": {
                        "id": 27711,
                        "name": "Berlanti Productions"
                    }
                }
            ]
        },
        {
            "id": 961323,
            "title": "Нимона",
            "tagline": "Новый герой обретает форму.",
            "overview": "Рыцарь, обвиненный в трагическом преступлении, объединяется с беспутным подростком-оборотнем, чтобы доказать свою невиновность.",
            "vote_average": 7.900000095367432,
            "release_date": "2023-06-23",
            "poster_path": "/2NQljeavtfl22207D1kxLpa4LS3.jpg",
            "genres": [
                {
                    "genre": {
                        "id": 12,
                        "name": " Приключение"
                    }
                },
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
                        "id": 10751,
                        "name": " Семья"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 13184,
                        "name": "Annapurna Pictures"
                    }
                },
                {
                    "company": {
                        "id": 31922,
                        "name": "DNEG Animation"
                    }
                }
            ]
        },
        {
            "id": 976573,
            "title": "Элементаль",
            "tagline": "Противоположности реагируют.",
            "overview": "В городе, где обитатели огня, воды, земли и воздуха живут вместе, пылкая молодая женщина и плывущий по течению парень откроют для себя нечто элементарное: как много у них общего.",
            "vote_average": 7.664000034332275,
            "release_date": "2023-06-14",
            "poster_path": None,
            "genres": [
                {
                    "genre": {
                        "id": 16,
                        "name": " Анимация"
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
                        "id": 10751,
                        "name": " Семья"
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
                        "id": 10749,
                        "name": " Романтика"
                    }
                },
                {
                    "genre": {
                        "id": 12,
                        "name": " Приключение"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 2,
                        "name": "Walt Disney Pictures"
                    }
                },
                {
                    "company": {
                        "id": 3,
                        "name": "Pixar"
                    }
                }
            ]
        },
        {
            "id": 980489,
            "title": "Gran Turismo",
            "tagline": "От геймера до гонщика.",
            "overview": "Настоящая история об исполнении желаний подростка, играющего в Gran Turismo, чьи игровые навыки позволили ему принять участие в серии соревнований Nissan и стать настоящим профессиональным автогонщиком.",
            "vote_average": 7.86299991607666,
            "release_date": "2023-08-09",
            "poster_path": "/51tqzRtKMMZEYUpSYkrUE7v9ehm.jpg",
            "genres": [
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
                },
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 125281,
                        "name": "PlayStation Productions"
                    }
                },
                {
                    "company": {
                        "id": 84792,
                        "name": "2.0 Entertainment"
                    }
                },
                {
                    "company": {
                        "id": 5,
                        "name": "Columbia Pictures"
                    }
                }
            ]
        },
        {
            "id": 1010581,
            "title": "Моя вина",
            "tagline": None,
            "overview": "Ной должна покинуть свой город, парня и друзей, чтобы переехать в особняк Уильяма Лейстера, яркого и богатого мужа ее матери Рафаэлы. Гордый и независимый 17-летний Ной отказывается жить в особняке, окруженном роскошью. Однако именно там она встречает Ника, своего нового сводного брата, и столкновение их сильных личностей становится очевидным с самого начала.",
            "vote_average": 7.993000030517578,
            "release_date": "2023-06-08",
            "poster_path": None,
            "genres": [
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                },
                {
                    "genre": {
                        "id": 10749,
                        "name": " Романтика"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 32485,
                        "name": "Pokeepsie Films"
                    }
                },
                {
                    "company": {
                        "id": 20580,
                        "name": "Amazon Studios"
                    }
                }
            ]
        },
        {
            "id": 1026227,
            "title": "Завтра еще есть",
            "tagline": None,
            "overview": "В послевоенной Италии семья типичной домохозяйки Делии находится в смятении из-за предстоящей помолвки любимого первенца Марселлы. Однако появление загадочного письма придаст Делии мужества встретиться лицом к лицу со своим жестоким мужем и представить себе лучшее будущее.",
            "vote_average": 8.199999809265137,
            "release_date": "2023-10-26",
            "poster_path": None,
            "genres": [
                {
                    "genre": {
                        "id": 35,
                        "name": " Комедия"
                    }
                },
                {
                    "genre": {
                        "id": 18,
                        "name": " Драма"
                    }
                }
            ],
            "companies": [
                {
                    "company": {
                        "id": 21246,
                        "name": "Wildside"
                    }
                },
                {
                    "company": {
                        "id": 115535,
                        "name": "Vision Distribution"
                    }
                },
                {
                    "company": {
                        "id": 213972,
                        "name": "Sky Studios"
                    }
                }
            ]
        }
    ]
    with mock.patch('handlers.pop.get_pop_based', return_value=movies) as mock_get_pop_based:
        message = AsyncMock()
        await start_pop(message)

        assert mock_get_pop_based.call_count == 1
        assert mock_get_pop_based.call_args == mock.call()

        media = await show_group_movies(movies)
        movies_poster_path_none = list(filter(lambda movie: movie['poster_path'] is None, movies))
        text_reply = await show_text_movies(movies_poster_path_none)

        message.reply_media_group.assert_awaited_with(media=media[10:])
        message.reply.assert_awaited_with(text_reply, parse_mode="HTML")
