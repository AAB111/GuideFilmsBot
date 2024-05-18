import aiohttp


async def get_pop_based(params: dict = None):
    if params is None:
        params = {"page": 1,
                  "n": 20}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/pop_based', params=params) as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def get_content_based(user_id: int, params: dict = None):
    if params is None:
        params = {"page": 1,
                  "n": 10}
    try:
        params['user_id'] = user_id
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/content_based', params=params) as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def request_auth(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            data = {'user_id': user_id}
            async with session.post("http://localhost:8000/user/create", json=data) as response:
                return response.status
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def get_search_movies(overview: str):
    try:
        async with aiohttp.ClientSession() as session:
            data = {'overview': overview}
            params = {'page': 1, 'n': 8}
            async with session.post("http://localhost:8000/search_movie", json=data, params=params) as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def get_movies_by_title(title: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/movie/by_title/{title}") as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def delete_movie_from_list(list_name: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"http://localhost:8000/user/movie/{list_name}", json=data) as response:
                return response.status
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def get_movie_from_list(list_name: str, params: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/user/{params['user_id']}/movie/{list_name}") as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def add_movie_to_list(list_name: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://localhost:8000/user/movie/{list_name}", json=data) as response:
                return response.status
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def patch_movie_from_list(list_name: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"http://localhost:8000/user/movie/{list_name}", json=data) as response:
                return response.status
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def get_credits_by_id(movie_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/movie/{movie_id}/credits/") as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def get_movie_by_id(movie_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/movie/by_id/{movie_id}") as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def get_similar_movies(movie_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            data_req = {'movie_id': movie_id}
            async with session.post(f"http://localhost:8000/content_based/", json=data_req) as response:
                return {'status': response.status, 'data': await response.json()}
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}


async def check_user(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            data_req = {'user_id': user_id}
            async with session.post(f"http://localhost:8000/user/check", json=data_req) as response:
                return response.status
    except Exception as e:
        print(e)
        return {'status': 500, 'data': None}
