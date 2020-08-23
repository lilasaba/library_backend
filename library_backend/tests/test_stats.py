import http.client

from faker import Faker

from books_backend.stats_namespace import get_books_per_entity

fake = Faker()


def generate_books(author='Some Body', n=5):
    for i in range(n):
        new_book = {'title': fake.text(100),
                    'book_count': i,
                    'year': 2000,
                    'author': author,
                    'publisher': fake.text(30)
                    }
        yield new_book


def test_book_count_per_author(client, delete_fixture):
    author = 'First Last'
    for new_book in generate_books(author=author):
        print(new_book)
        response = client.post('/admin/add_book/', data=new_book)
        assert http.client.CREATED == response.status_code

    book_counts = get_books_per_entity(author, 'author')
    print(author, book_counts)
    assert book_counts == sum(range(5))


def test_get_books_per_author(client, book_fixture):#, delete_fixture):
    response = client.get('/stats/all_stats/')
    # assert http.client.OK == response.status_code
    print(response.__dict__)
    result = response.json
    print(result)
