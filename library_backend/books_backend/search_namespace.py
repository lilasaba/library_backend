from flask_restplus import Namespace, Resource

from books_backend.admin_namespace import book_model
from books_backend.models import AuthorModel, BookModel, PublisherModel
from books_backend.db import db

search_namespace = Namespace('search', description='Post and delete books.')

# Search args.
search_parser = search_namespace.parser()
search_parser.add_argument('title', type=str, required=False,
                           help='Title of the book')
search_parser.add_argument('book_count', type=int, required=False,
                           help='Nr of books')
search_parser.add_argument('year', type=int, required=False,
                           help='Year of the book')
search_parser.add_argument('author', type=str, required=False,
                           help='Author of the book')
search_parser.add_argument('publisher', type=str, required=False,
                           help='Publisher of the book')
search_parser.add_argument('id', type=str, required=False,
                           help='ID of the book')


def get_name_id(name, name_type):
    entry_id = None
    if name_type == 'author':
        table_model = AuthorModel
    elif name_type == 'publisher':
        table_model = PublisherModel

    try:
        entry_id = db.session.query(table_model)\
                                   .filter(table_model.name == name).one().id
    except Exception as e:
        # TODO: log this.
        # print(f'Exception {e} for {name} with {name_type}.')
        e = f'{e}'
        pass

    return entry_id


@search_namespace.route('/books/')
class SearchBooks(Resource):

    @search_namespace.doc('search_books')
    @search_namespace.marshal_with(book_model, as_list=True)
    @search_namespace.expect(search_parser)
    def get(self):
        '''
        Search books by their attributes.
        '''
        args = search_parser.parse_args()
        title_param = args['title']
        book_count_param = args['book_count']
        year_param = args['year']
        id_param = args['id']
        # author_param = args['author']
        # publisher_param = args['publisher']
        # TODO: add time_in.

        query = db.session.query(BookModel)
        if title_param:
            param = f'%{title_param}%'
            query = (query.filter(BookModel.title.ilike(param)))
            # Old code, that it's not case insensitive in postgreSQL.
            # query = (query.filter(BookModel.title.contains(title_param)))
        elif book_count_param:
            query = query.filter(BookModel.book_count == int(book_count_param))
        elif year_param:
            query = query.filter(BookModel.year == int(year_param))
        elif id_param:
            query = query.filter(BookModel.id == int(id_param))

        query = query.order_by('id')
        books = query.all()

        return books
