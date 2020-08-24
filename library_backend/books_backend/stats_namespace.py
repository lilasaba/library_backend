from flask import jsonify
from flask_restplus import Namespace, Resource

from books_backend.db import db
from books_backend.models import (AuthorModel,
                                  # AverageAgeOfBooksModel,
                                  # AverageTimeToLibraryPerAuthorModel,
                                  # BookCountOfThirdBookPerAuthorModel,
                                  # BooksPerPublisherModel,
                                  # OldestAndYoungestBookModel,
                                  # PublisherModel)
                                  BookModel,
                                  BooksPerAuthorModel)
from books_backend.search_namespace import get_name_id

stats_namespace = Namespace('stats', description='Generate db stats.')


def get_books_per_entity(entity, entity_type):
    entity_id = get_name_id(entity, entity_type)
    # if entity_type == 'author':
    # eid_var = 'author_id'
    # elif entity_type == 'publisher':
    # eid_var = 'publisher_id'
    # TODO: author_id column as variable.
    try:
        book_counts = db.session.query(BookModel.book_count).filter(
                                      (BookModel.author_id == entity_id)).all()
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
    pass


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
        Generate multiple statistics from the db.
        TODO: finish this.
        '''
        books_per_author = {}
        authors = db.session.query(AuthorModel.name).all()
        for author in authors:
            author = author[0]
            counts = get_books_per_entity(author, 'author')
            books_per_author[author] = counts
        add_to_table(books_per_author, BooksPerAuthorModel, 'author')

        return jsonify(books_per_author)
