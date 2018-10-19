import re
import logging
from bs4 import BeautifulSoup

from locators.all_books_page import AllbooksPageLocators
from locators.book_pages_locator import NUMBER_OF_PAGES
from parsers.book_parser import BookParser


logger = logging.getLogger('scraping.all_books_page')

class AllBooksPage:
    def __init__(self, page_content):
        logger.debug('Parsing page content with BeautifulSoup parser')
        self.soup = BeautifulSoup(page_content, 'html.parser')

    @property
    def books(self):
        logger.debug(f'finding all books in page using `{AllbooksPageLocators.BOOKS}`.')
        return [BookParser(e) for e in self.soup.select(AllbooksPageLocators.BOOKS)]

    @property
    def num_of_pages(self):
        logging.debug('Finding all number of catalogue pages available')
        pattern = re.compile('(\d+)(?!.*\d)')
        num_of_pages = self.soup.select_one(NUMBER_OF_PAGES)
        logger.info(f'Found number of catalogue pages available: `{num_of_pages}`')
        number = int(re.search(pattern, num_of_pages.text.strip()).group(0))
        logger.debug(f'Extracted number of pages as integer: `{number}`')
        return number



