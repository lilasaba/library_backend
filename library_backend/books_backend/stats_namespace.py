from flask import jsonify
from flask_restplus import Namespace, Resource
from sqlalchemy import and_

from books_backend.db import db
from books_backend.models import (AuthorModel,
                                  AverageAgeOfBooksModel,
                                  AverageTimeToLibraryPerAuthorModel,
                                  BookCountOfThirdBookPerAuthorModel,
                                  BookModel,
                                  BooksPerAuthorModel,
                                  BooksPerPublisherModel,
                                  OldestAndYoungestBookModel,
                                  PublisherModel)
from books_backend.search_namespace import get_name_id, id_to_name

stats_namespace = Namespace('stats', description='Generate db stats.')


def get_books_per_entity(entity, entity_type):
    entity_id = get_name_id(entity, entity_type)
    if entity_type == 'author':
        table_model = AuthorModel
    elif entity_type == 'publisher':
        table_model = PublisherModel
    try:
        book_counts = db.session.query(BookModel.book_count).filter(
                                      (table_model.id == entity_id)).all()
    except Exception as e:
        # TODO: log this.
        # print(f'Exception {e} for {name} with {name_type}.')
        e = f'{e}'
        books_per_entity = 0

    books_per_entity = sum([bc[0] for bc in book_counts])

    return books_per_entity


def add_to_table(fields, table, entity_type):
    objects = []
    for entity, counts in fields.items():
        entity_id = get_name_id(entity, entity_type)
        objects.append(table(entity_id=entity_id, book_count=counts))

    # Bulk add to table.
    db.session.bulk_save_objects(objects)
    db.session.commit()


def get_average_age_of_books():
    try:
        years = db.session.query(BookModel.year)
        time_ins = db.session.query(BookModel.time_in)
        book_counts = db.session.query(BookModel.book_count)
    except Exception as e:
        # TODO: log this.
        # print(f'Exception {e} for {name} with {name_type}.')
        e = f'{e}'


def get_oldest_and_youngest_book():
    pass


def get_average_time_to_library_per_author(author):
    pass


def get_book_count_of_third_book_per_author(author):
    pass


@stats_namespace.route('/all_stats/')
class GetStats(Resource):

    @stats_namespace.doc('stats_books')
    def get(self):
        '''
        '''
        books_per_author = {}
        authors = db.session.query(AuthorModel.name).all()
        for author in authors:
            author = author[0]
            counts = get_books_per_entity(author, 'author')
            books_per_author[author] = counts
        add_to_table(books_per_author, BooksPerAuthorModel, 'author')


        return jsonify(books_per_author)
