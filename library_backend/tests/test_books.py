import http.client
import random

from faker import Faker
from unittest.mock import ANY

fake = Faker()


def test_add_book(client):
    new_book = {'title': fake.text(100),
                'book_count': random.randint(1, 10),
                'year': 2000,
                'author': fake.text(40),
                'publisher': fake.text(30)
                }
    response = client.post('/admin/add_book/', data=new_book)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {'id': ANY,
                'title': new_book['title'],
                'book_count': new_book['book_count'],
                'year': new_book['year'],
                'time_in': ANY,
                'author_id': ANY,
                'publisher_id': ANY,
                }
    assert result == expected


def test_list_books(client, book_fixture):
    response = client.get('/admin/books/')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the ids are increasing.
    previous_id = -1
    for book in result:
        expected = {'id': ANY,
                    'title': ANY,
                    'book_count': ANY,
                    'year': ANY,
                    'time_in': ANY,
                    'author_id': ANY,
                    'publisher_id': ANY
                    }
        assert expected == book
        assert book['id'] > previous_id
        previous_id = book['id']


def test_list_books_search(client, book_fixture):
    new_book = {'title': 'A tale about a Platypus',
                'book_count': random.randint(1, 10),
                'year': 2000,
                'author': fake.text(40),
                'publisher': fake.text(30)
                }

    response = client.post('/admin/add_book/', data=new_book)
    assert http.client.CREATED == response.status_code

    response = client.get('/admin/books/?search=platypus')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the returned values contain "platypus".
    for book in result:
        expected = {'id': ANY,
                    'title': ANY,
                    'book_count': ANY,
                    'year': ANY,
                    'time_in': ANY,
                    'author_id': ANY,
                    'publisher_id': ANY
                    }
        assert expected == book
        assert 'platypus' in book['title'].lower()


def test_get_book(client, book_fixture):
    book_id = book_fixture[0]
    response = client.get(f'/admin/books/{book_id}/')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'id' in result
    assert 'title' in result
    assert 'year' in result
    assert 'author_id' in result


def test_get_non_existing_book(client, book_fixture):
    book_id = 123456
    response = client.get(f'/admin/books/{book_id}/')

    assert http.client.NOT_FOUND == response.status_code
