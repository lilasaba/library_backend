from sqlalchemy import func, ForeignKey
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
    #year = db.Column(db.Date)
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

