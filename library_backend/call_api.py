import http.client
import json
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
print('XXXXXXXXXXXXXXX')


def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    application.db.create_all()

    return application


def call_admin_add_book():
    '''
    Add books.
    '''

    print('YYYYYYYYYYYYYYYYYYY')
    book_ids = []
    for _ in range(3):
        book = {'title': fake.text(100),
                'author': fake.text(40),
                'publisher': fake.text(30),
                'time_in': datetime.utcnow(),
                'year': 2000
        }
        print(book)
        response = requests.post(f'{endpoint}/add_book/', data=book)
        #response = client.post('/api/me/books/', data=book,
        #assert http.client.CREATED == response.status_code
        result = eval(response.content)
        #result = response.json
        print(result)
        print(response.__dict__)
        book_ids.append(result['id'])


    # Get and delete all books.
    response = requests.get(f'{endpoint}/books/')
    #response = client.get('/api/books/')
    books = eval(response.content)
    #books = response.json
    for book in books:
        book_id = book['id']
        url = f'/admin/books/{book_id}/'
        response = requests.delete(f'{endpoint}{url}')
        #response = client.delete(f'{endpoint}{url}')
        #response = client.delete(url)
        print(response.__dict__)
        #assert http.client.NO_CONTENT == response.status_code


if __name__ == '__main__':
    call_admin_add_book()
