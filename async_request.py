import aiohttp
import async_timeout
import asyncio
import time

all_times = []

async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            all_times.append(time.time() - page_start)
            return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks

loop = asyncio.get_event_loop()
urls = ['https://www.tulipdragon.com/' for i in range(50)]
loop.run_until_complete(get_multiple_pages(loop, *urls))
print(sum(all_times)/len(all_times))
