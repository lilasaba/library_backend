# Library Backend

## Set up

### Create a virtual environment and install the requirements

    $ python3 -m venv ./venv
    $ source ./venv/bin/activate
    $ pip install -r requirements.txt

### Get the local database ready

    $ python init_db.py

### Start the development server

    $ FLASK_APP=wsgi.py flask run

## Tests

## Run the unit tests with

    $ pytest

## Dependencies

`library_backend` uses Flask as a web framework, Flask RESTplus for creating the interface, and SQLAlchemy to handle the database models. It uses a SQLlite database for local development and PostgreSQL for production.
