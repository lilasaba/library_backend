import csv
import http.client
import random
import requests
import time

from faker import Faker

fake = Faker()
endpoint = 'http://0.0.0.0:8000/admin'
endpoint = 'http://0.0.0.0:5000/admin'
endpoint_search = 'http://0.0.0.0:5000/search'


def read_in_data():
    c = 0
    with open('data/lib_books.tsv') as inf:
        for line in csv.reader(inf, delimiter='\t'):
            if c > 0:
                if random.randint(1, 10) < 2:
                    book = {'title': line[1],
                            'book_count': random.randint(1, 10),
                            'year': int(line[3]),
                            'author': line[2],
                            'publisher': line[4],
                            }
                    print(book)
                    yield book
            c += 1


def call_admin_add_book():
    '''
    Add books.
    '''
    for book in read_in_data():
        response = requests.post(f'{endpoint}/add_book/', data=book)
        assert http.client.CREATED == response.status_code
        # result = eval(response.content)
        # print(result)
        time.sleep(0.3)


def call_admin_list_books():
    '''
    List all books.
    '''
    response = requests.get(f'{endpoint}/books/')
    result = eval(response.content)

    return result


def call_title_search():
    new_book = {'title': 'Another tale about a Platypus',
                'book_count': random.randint(1, 10),
                'year': 2000,
                'author': fake.text(40),
                'publisher': fake.text(30)
                }

    response = requests.post(f'{endpoint}/add_book/', data=new_book)
    assert http.client.CREATED == response.status_code

    response = requests.get(f'{endpoint_search}/books/?title=platypus')
    result = eval(response.content)

    assert http.client.OK == response.status_code

    # Check that the returned values contain "platypus".
    for book in result:
        print('BOOK RESULT', book)
        assert 'platypus' in book['title'].lower()


if __name__ == '__main__':
    # call_admin_add_book()
    # added_books = call_admin_list_books()
    # print(added_books[:100])
    # print(len(added_books))
    call_title_search()
