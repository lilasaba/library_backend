import csv
import http.client
import random
import requests

from faker import Faker

fake = Faker()
endpoint = 'http://0.0.0.0:8000/admin'


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

    book_ids = []
    for book in read_in_data():
        response = requests.post(f'{endpoint}/add_book/', data=book)
        assert http.client.CREATED == response.status_code
        result = eval(response.content)
        book_ids.append(result['id'])

    # Get and delete all books.
    response = requests.get(f'{endpoint}/books/')
    books = eval(response.content)

    return books
#    for book in books:
#        book_id = book['id']
#        url = f'/books/{book_id}/'
#        response = requests.delete(f'{endpoint}{url}')
#        assert http.client.NO_CONTENT == response.status_code


if __name__ == '__main__':
    added_books = call_admin_add_book()
    print(added_books[:100])
    print(len(added_books))
