import http.client
import json
import random
import requests
import sys

sys.path.insert(0, 'books_backend')
sys.path.insert(0, 'tests')

from datetime import datetime
from faker import Faker

from tests.constants import PRIVATE_KEY
from books_backend.app import create_app

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
        print(book)
        print(json.dumps(book))
        response = requests.post(f'{endpoint}/add_book/', data=book)
        assert http.client.CREATED == response.status_code
        print(response.__dict__)
        result = eval(response.content)
        print(result)
        book_ids.append(result['id'])

    # Get and delete all books.
    response = requests.get(f'{endpoint}/books/')
    #response = client.get('/api/books/')
    books = eval(response.content)
    #books = response.json
    for book in books:
        book_id = book['id']
        url = f'/books/{book_id}/'
        response = requests.delete(f'{endpoint}{url}')
        print(response.__dict__)
        assert http.client.NO_CONTENT == response.status_code


if __name__ == '__main__':
    call_admin_add_book()
