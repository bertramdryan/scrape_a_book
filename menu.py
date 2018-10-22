from app import bookpages

USER_CHOICE = '''Enter one of the following:

- 'b' to look at 5-star books
- 'c' to look at the cheapest books
- 'l' to print out all books
- 'n' to just get next available book on page
- 'q' to exit
Enter your choice: '''


def print_five_star_books():
    for book in bookpages:
        if book.rating == 5:
            print(book)


def print_cheapest_books():
    cheapest_books = sorted(bookpages, key=lambda x: x.price)
    for book in cheapest_books:
        print(book)


def print_all_books():
    for book in bookpages:
        print(book)

    print(f'{len(bookpages)} total books.')


book_generator = (x for x in bookpages)


def print_next_book():
    print(next(book_generator))


user_choice = {
    'b': print_five_star_books,
    'c': print_cheapest_books,
    'l': print_all_books,
    'n': print_next_book
}


def menu():
    answer = input(USER_CHOICE)

    while answer != 'q':
        if answer in ('b', 'c', 'l','n'):
            user_choice[answer]()
        else:
            print('print a valid command.')
        answer = input(USER_CHOICE)


menu()
