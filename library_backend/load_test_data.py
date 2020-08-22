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
        author = AuthorModel(name=fake.text(40))
        publisher = PublisherModel(name=fake.text(40))

        # Create author entry.
        application.db.session.add(author)
        application.db.session.flush()
        application.db.session.refresh(author)
        author_id = author.id
        application.db.session.commit()

        # Create publisher entry.
        application.db.session.add(publisher)
        application.db.session.flush()
        application.db.session.refresh(publisher)
        publisher_id = publisher.id
        application.db.session.commit()

        # Create book entry.
        book = BookModel(title=fake.text(100),
                         book_count=random.randint(1, 10),
                         year=2000,
                         author_id=author_id,
                         publisher_id=publisher_id)
        application.db.session.add(book)
        application.db.session.flush()
        application.db.session.commit()

    application.db.session.close()

