"""Create pytest fixtures that set up flask application, database, and test client,
passing the output of the functions to the test functions as reusable components."""

import pytest
from main import create_app
from extensions import db


@pytest.fixture(scope="module")  # scope='module' ensures fixture is created once
# per module (file) instead of per test function
def app():
    """Create a Flask application for testing, using the test configuration
    defined in config.py (sqlite in-memory database)."""

    app = create_app("config.TestConfig")  # Using TestConfig to setup app with sqlite
    with app.app_context():
        db.create_all()  # Creates all tables in the in-memory database
    yield app  # Passes the app instance to the test functions
    with app.app_context():
        db.drop_all()  # Drops all tables after tests are done


@pytest.fixture
def client(app):
    """Create a test HTTP client for the Flask application, similar to insomnia,
    capable of making HTTP requests and process responses without running the server."""

    return app.test_client()


@pytest.fixture
def db_session(app):
    """Create a database session for testing."""

    with app.app_context():
        yield db.session  # Passes the database session to test functions
        db.session.rollback()  # Undo any changes to the database after each test
