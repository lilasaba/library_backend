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

# Stats args.
stats_parser = stats_namespace.parser()
stats_parser.add_argument('author', type=str, required=False,
                           help='Nr of books per author.')


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

    print(entity, book_counts)
    books_per_entity = sum([bc[0] for bc in book_counts])

    return books_per_entity


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
    @stats_namespace.expect(stats_parser)
    def get(self):
        '''
        '''
        args = stats_parser.parse_args()

        query = db.session.query(BookModel)

        query = query.order_by('id')
        stats = query.all()

        return stats
