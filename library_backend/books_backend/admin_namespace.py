import http.client

from datetime import datetime
from flask_restplus import fields, Namespace, Resource
from books_backend.models import AuthorModel, BookModel, PublisherModel
from books_backend.db import db

admin_namespace = Namespace('admin', description='Post and delete books.')

# Book args.
book_parser = admin_namespace.parser()
book_parser.add_argument('title', type=str, required=True,
                          help='Title of the book')
book_parser.add_argument('year', type=int, required=True,
                          help='Year of the book')
book_parser.add_argument('time_in', type=str, required=True,
                          help='Adding time of the book')
book_parser.add_argument('author', type=str, required=True,
                          help='Author of the book')
book_parser.add_argument('publisher', type=str, required=True,
                          help='Publisher of the book')
# Search args.
search_parser = admin_namespace.parser()
search_parser.add_argument('search', type=str, required=False,
                            help='Search in the titles of the books.')

model = {
    'id': fields.Integer(),
    'title': fields.String(),
    'year': fields.Integer(),
    'time_in': fields.DateTime(),
    'author': fields.String(),
    'publisher_id': fields.String(),
}
#book_model = admin_namespace.model('Book', model)


def get_name_id(name, name_type):
    entry_id = None
    if name_type == 'author':
        table_model = AuthorModel
    elif name_type == 'publisher':
        table_model = PublisherModel

    try:
        entry_id = db.session.query(table_model)\
                                   .filter(table_model.name==name).one().id
    except Exception as e:
        # TODO: log this.
        print(f'Exception {e} for {name} with {name_type}.')

    if not entry_id:
        entry = table_model(name=name)
        db.session.add(entry)
        db.session.flush()
        db.session.refresh(entry)
        entry_id = entry.id
        db.session.commit()

    return entry_id


@admin_namespace.route('/add_book/')
class AddBook(Resource):
    @admin_namespace.doc('create_book')
    @admin_namespace.expect(book_parser)
    #@admin_namespace.marshal_with(book_model, code=http.client.CREATED)
    def post(self):
        '''
        Create a new book.
        '''
        args = book_parser.parse_args()
        author = args['author']
        publisher = args['publisher']
        year = args['year']

        # Get author- and publisher ids.
        author_id = get_name_id(author, 'author')
        publisher_id = get_name_id(publisher, 'publisher')

        new_book = BookModel(title=args['title'],
                             time_in=args['time_in'],
                             year=(year, 1, 1),
                             author_id=author_id,
                             publisher_id=publisher_id)
        db.session.add(new_book)
        db.session.flush()
        db.session.commit()

        #result = api_namespace.marshal(new_book, book_model)
        result = new_book

        return result, http.client.CREATED


@admin_namespace.route('/books/')
class ListBooks(Resource):

    @admin_namespace.doc('list_books')
    #@admin_namespace.marshal_with(book_model, as_list=True)
    @admin_namespace.expect(search_parser)
    def get(self):
        '''
        Retrieve all books.
        '''
        args = search_parser.parse_args()
        search_param = args['search']
        query = BookModel.query
        if search_param:
            param = f'%{search_param}%'
            query = (query.filter(BookModel.title.ilike(param)))
            # Old code, that it's not case insensitive in postgreSQL.
            # query = (query.filter(BookModel.title.contains(search_param)))

        query = query.order_by('id')
        books = query.all()

        return books


@admin_namespace.route('/books/<int:book_id>/')
class RetrieveBook(Resource):

    @admin_namespace.doc('retrieve_book')
    #@admin_namespace.marshal_with(book_model)
    def get(self, book_id):
        '''
        Retrieve a book by id.
        '''
        book = BookModel.query.get(book_id)
        if not book:
            # The book is not present
            return '', http.client.NOT_FOUND

        return book


@admin_namespace.route('/delete_book/<int:book_id>/')
class DeleteBook(Resource):

    @admin_namespace.doc('delete_book',
                         responses={http.client.NO_CONTENT: 'No content'})
    def delete(self, book_id):
        '''
        Delete a book.
        '''
        book = BookModel.query.get(book_id)
        if not book:
            # The book is not present.
            return '', http.client.NO_CONTENT

        db.session.delete(book)
        db.session.commit()

        return '', http.client.NO_CONTENT
