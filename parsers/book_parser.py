import re
import logging

from locators.book_locators import BookLocators

logger = logging.getLogger('scrapping.book_parser')


class BookParser:
    """
    A class to take in an HTML page (or part of it) and find property of an
    item in it
    """
    RATINGS = {
        'Zero': 0,
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        logging.info(f'New book parser created from `{parent}`')
        self.parent = parent

    def __repr__(self):
        return f'<Book {self.name}, £{self.price} ({self.rating} {"stars" if self.rating != 1 else "star"})>'

    @property
    def name(self) -> str:
        logger.debug('Finding book name...')
        locator = BookLocators.NAME_LOCATOR
        item_name = self.parent.select_one(locator).attrs['title']
        logger.debug(f'Found book by the name of `{item_name}`')
        return item_name

    @property
    def page_link(self) -> str:
        logger.debug('Finding book link...')
        locator = BookLocators.LINK_LOCATOR
        item_url = self.parent.select_one(locator).attrs['href']
        return item_url


    @property
    def price(self) -> float:
        logger.debug('Finding book price...')
        locator = BookLocators.PRICE_LOCATOR
        item_price = self.parent.select_one(locator).string
        pattern = '£([0-9]+\.[0-9]+)'
        matcher = re.search(pattern, item_price)
        return float(matcher.group(1))

    @property
    def rating(self) -> int:
        locator = BookLocators.RATING_LOCATOR
        star_rating_element = self.parent.select_one(locator)
        classes = star_rating_element.attrs['class']
        rating_classes = [r for r in classes if r != 'star-rating']
        rating_number = BookParser.RATINGS.get(rating_classes[0])
        return rating_number
