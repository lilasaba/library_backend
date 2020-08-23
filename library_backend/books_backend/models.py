from sqlalchemy import func
from books_backend.db import db


def generate_date():
    pass


class BookModel(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(450))
    book_count = db.Column(db.Integer)
    year = db.Column(db.Integer)
    # TODO: Date object is not JSON serializable.
    # year = db.Column(db.Date)
    time_in = db.Column(db.DateTime, server_default=func.now())
    # TODO: make authors column a tuple.
    author_id = db.Column(db.ForeignKey('author.id'))
    publisher_id = db.Column(db.ForeignKey('publisher.id'))


class AuthorModel(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))


class PublisherModel(db.Model):
    __tablename__ = 'publisher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))


class BooksPerAuthorModel(db.Model):
    __tablename__ = 'books_per_author'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey('author.id'))
    book_count = db.Column(db.Integer)


class BooksPerPublisherModel(db.Model):
    __tablename__ = 'books_per_publisher'
    id = db.Column(db.Integer, primary_key=True)
    publisher_id = db.Column(db.ForeignKey('publisher.id'))
    book_count = db.Column(db.Integer)


class AverageAgeOfBooksModel(db.Model):
    __tablename__ = 'average_age_of_books'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey('book.id'))
    age = db.Column(db.Integer)


class OldestAndYoungestBookModel(db.Model):
    __tablename__ = 'oldest_and_youngest_book'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.ForeignKey('book.id'))
    year = db.Column(db.Integer)


class AverageTimeToLibraryPerAuthorModel(db.Model):
    __tablename__ = 'average_time_to_library_per_author'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey('author.id'))
    time_to_lib = db.Column(db.Integer)


class BookCountOfThirdBookPerAuthorModel(db.Model):
    __tablename__ = 'book_count_of_third_book_per_author'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.ForeignKey('author.id'))
    book_count = db.Column(db.Integer)
