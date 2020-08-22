import http.client
import random
import requests

from faker import Faker

fake = Faker()
endpoint = 'http://0.0.0.0:5030/admin'


def call_admin_add_book():
    '''
    Add books.
    '''

    book_ids = []
    for _ in range(3):
        book = {'title': fake.text(100),
                'book_count': random.randint(1, 10),
                'year': 2000,
                'author': fake.text(40),
                'publisher': fake.text(30),
                }
        response = requests.post(f'{endpoint}/add_book/', data=book)
        assert http.client.CREATED == response.status_code
        result = eval(response.content)
        book_ids.append(result['id'])

    # Get and delete all books.
    response = requests.get(f'{endpoint}/books/')
    books = eval(response.content)
    for book in books:
        book_id = book['id']
        url = f'/books/{book_id}/'
        response = requests.delete(f'{endpoint}{url}')
        assert http.client.NO_CONTENT == response.status_code


if __name__ == '__main__':
    call_admin_add_book()
