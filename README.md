[![Build Status](https://travis-ci.com/lilasaba/library_backend.svg?branch=master)](https://travis-ci.com/lilasaba/library_backend)

# Book Library Backend

Containerized Python Flask API served by PostgreSQL utilizing SQLAlchemy db toolkit.

A book library application that stores books with the following attributes:

+ title
+ author
+ publisher
+ year
+ book count
+ time in (generated at adding time)

## Architecture

### App

Flask application in `library_backend/books_backend`.
Details in [readme](library_backend/README.md).

#### Testing

`library_backend/tests` with pytest

#### Docker

`docker/app/Dockerfile`

### DB

#### Local

SQLite

#### Server

PostgreSQL

#### Docker

`docker/db/Dockerfile`

### CI

Powered by `.travis.yml`: only build and test, deploy to dockerhub is in
progress.

### Dependencies

+ Python 3.6+
+ docker
+ docker-compose

#### Tested with

```
$ python --version
Python 3.8.5
$ docker --version
Docker version 18.06.0-ce, build 0ffa825
$ docker-compose --version
docker-compose version 1.24.0-rc1, build 0f3d4dda
```

### Build and launch db and application

```
docker-compose build db
docker-compose build test-postgresql
docker-compose run test-postgresql
docker-compose build test
docker-compose run test
docker-compose build static-analysis
docker-compose run static-analysis
docker-compose build server
docker-compose run -p 127.0.0.1:8000:8000/tcp server
```

### Documentation/Swagger

Inspect in local browser at `127.0.0.1:8000`.

## Usage

### Add data

### Add single book

```
import requests

new_book = {'title': 'Some Title',
            'book_count': 4,
            'year': 2000,
            'author': 'Some Author',
            'publisher': 'Some Publisher'
            }

response = requests.post(f'http://0.0.0.0:8000:admin/add_book/', data=new_book)
```

### Add tsv data

```
import requests
import time

endpoint = 'http://0.0.0.0:8000/admin'
endpoint_search = 'http://0.0.0.0:8000/search'


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


# Add and list books.
call_admin_add_book()
added_books = call_admin_list_books()
print(added_books[:100])
print(len(added_books))
```

### Search for book

#### By title

```
title = 'Some Title'
response = requests.get(f'http://0.0.0.0:8000:search/books/?title={title}')
print(response.content)
print(response.status_code)
```

#### By author

```
author = 'Some Author'
response = requests.get(f'http://0.0.0.0:8000:search/books/?author={author}')
print(response.content)
print(response.status_code)
```

#### By year
#### By book_count

### Get book library statistics

## References

+ [Hands-On-Docker-for-Microservices-with-Python](https://github.com/PacktPublishing/Hands-On-Docker-for-Microservices-with-Python)

## TODO's/Notes

* unique constraints missing: duplicate titles with different other column
  values are possible
* Statistics generation and tables are not finished :(
* RabbitMQ
