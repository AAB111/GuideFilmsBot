import aiohttp


async def request_auth(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            data = {'id': user_id}
            async with session.post("http://localhost:8000/user/create", json=data) as response:
                return response.status
    except Exception as e:
        print(e)


async def get_search_movies(overview: str, user_id: int):
    try:
        async with aiohttp.ClientSession() as session:
            data = {'overview': overview, 'user_id': user_id}
            async with session.post("http://localhost:8000/search_movie", json=data) as response:
                if response.status != 200:
                    return None
                return await response.json()
    except Exception as e:
        print(e)


async def get_movies_by_title(title: str):
    try:
        async with aiohttp.ClientSession() as session:
            params = {'title': title}
            async with session.get("http://localhost:8000/movie/", params=params) as response:
                if response.status != 200:
                    return None
                return await response.json()
    except Exception as e:
        print(e)


async def delete_movie_from_list(list_name: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"http://localhost:8000/user/movies/{list_name}", json=data) as response:
                return response.status
    except Exception as e:
        print(e)


async def get_movie_from_list(list_name: str, params: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/user/movies/{list_name}", params=params) as response:
                if response.status != 200:
                    return None
                return await response.json()
    except Exception as e:
        print(e)


async def add_movie_to_list(list_name: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"http://localhost:8000/user/movies/{list_name}", json=data) as response:
                return response.status
    except Exception as e:
        print(e)


async def patch_movie_from_list(list_name: str, data: dict):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(f"http://localhost:8000/user/movies/{list_name}", json=data) as response:
                return response.status
    except Exception as e:
        print(e)
