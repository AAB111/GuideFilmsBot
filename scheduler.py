import apscheduler
import asyncio
from aiogram import Bot
from aiogram.client.session import aiohttp
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def pop_based(bot: Bot):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/pop_based') as response:
            response_json = await response.json()
            # chat_list = await bot.get_chat_()
                # await bot.send_message(chat_id=,text=str(response_json))
def runner(bot: Bot):
    asyncio.run(pop_based(bot))

async def start_scheduler(bot: Bot):
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }

    scheduler = AsyncIOScheduler()
    scheduler.configure(executors=executors)
    scheduler.add_job(runner, "interval", seconds=30, executor="processpool", args=(Bot,))
    scheduler.start()
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Процесс прерван")

