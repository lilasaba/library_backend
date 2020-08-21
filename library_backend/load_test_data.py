from faker import Faker
import random

from books_backend.app import create_app
from books_backend.models import AuthorModel, BookModel, PublisherModel

fake = Faker()


if __name__ == '__main__':
    application = create_app()
    application.app_context().push()

    # Create test data.
    for i in range(5):
        book = BookModel(title=fake.text(100),
                         book_count=random.randint(1, 10),
                         year=2000,
                         author_id=i,
                         publisher_id=i)
        author = AuthorModel(id=i, name=fake.text(40))
        publisher = PublisherModel(id=i, name=fake.text(40))

        application.db.session.add(author)
        application.db.session.add(publisher)
        application.db.session.commit()
        application.db.session.add(book)
        application.db.session.commit()

    application.db.session.close()

