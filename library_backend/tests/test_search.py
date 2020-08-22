import http.client
import random

from faker import Faker
from unittest.mock import ANY

fake = Faker()


def test_title_search(client):
    new_book = {'title': 'Another tale about a Platypus',
                'book_count': random.randint(1, 10),
                'year': 2000,
                'author': fake.text(40),
                'publisher': fake.text(30)
                }

    response = client.post('/admin/add_book/', data=new_book)
    assert http.client.CREATED == response.status_code

    response = client.get('/search/books/?title=platypus')
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
                    'author': ANY,
                    'publisher': ANY
                    }
        assert expected == book
        assert 'platypus' in book['title'].lower()


def test_id_search(client, book_fixture):
    book_id = book_fixture[0]
    response = client.get(f'/search/books/?id={book_id}')
    result = response.json
    result = result[0]
    print(result)

    assert http.client.OK == response.status_code
    assert 'id' in result
    assert 'title' in result
    assert 'year' in result
    assert 'author' in result


def test_author_search(client):
    new_book = {'title': 'Some Title',
                'book_count': random.randint(1, 10),
                'year': 2000,
                'author': 'Some Person',
                'publisher': fake.text(30)
                }

    response = client.post('/admin/add_book/', data=new_book)
    assert http.client.CREATED == response.status_code

    author = new_book['author']
    response = client.get(f'/search/books/?author={author}')
    result = response.json
    result = result[0]
    print(result)

    assert http.client.OK == response.status_code
    assert 'author' in result
    assert 'publisher' in result
    assert result['author'] == author
