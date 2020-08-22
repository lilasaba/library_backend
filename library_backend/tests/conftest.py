import http.client
import pytest
import random

from faker import Faker

from books_backend.app import create_app

fake = Faker()


@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    application.db.create_all()

    return application


@pytest.fixture
def book_fixture(client):
    '''
    Generate three books in the system.
    '''

    book_ids = []
    for _ in range(3):
        book = {'title': fake.text(100),
                'book_count': random.randint(1, 10),
                'year': 2000,
                'author': fake.text(40),
                'publisher': fake.text(30)
                }
        response = client.post('/admin/add_book/', data=book)
        assert http.client.CREATED == response.status_code
        result = response.json
        book_ids.append(result['id'])

    yield book_ids

    # Delete all books.
    response = client.get('/admin/books/')
    books = response.json
    for book in books:
        book_id = book['id']
        url = f'/admin/books/{book_id}/'
        response = client.delete(url)
        assert http.client.NO_CONTENT == response.status_code
