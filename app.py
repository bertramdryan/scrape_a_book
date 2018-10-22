import aiohttp
import asyncio
import async_timeout
import time
import logging
import requests

from pages.all_books_page import AllBooksPage


loop = asyncio.get_event_loop()

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO,
                    filename='logs.txt')
logger = logging.getLogger('scraping')

logger.info('Loading books list...')

page_content = requests.get('http://books.toscrape.com').content
page = AllBooksPage(page_content)

bookpages = page.books

async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_multiple_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        grouped_tasks = asyncio.gather(*tasks)
        return await grouped_tasks

start = time.time()
number_of_pages = AllBooksPage(page_content).num_of_pages
urls = [f'http://books.toscrape.com/catalogue/page-{n + 1}.html' for n in range(1, number_of_pages)]
pages = loop.run_until_complete(get_multiple_pages(loop, *urls))


for page_content in pages:
    logger.debug('Creating AllBooksPage from page content.')
    page = AllBooksPage(page_content)
    bookpages.extend(page.books)

print(f'Total page requests too {time.time() - start}')



