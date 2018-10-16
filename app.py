import requests

from pages.all_books_page import AllBooksPage


page = AllBooksPage(page_content)
for n in range(50):
    page_content = requests.get('http://books.toscrape.com').content


books = page.books



