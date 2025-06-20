import os
import tempfile
import pytest
from todo_app import create_app
from todo_app import db as _db
from todo_app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False  # Disable CSRF tokens in the Forms
    })

    # Create the database and load test data
    with app.app_context():
        _db.create_all()

    yield app

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def db(app):
    """Create and configure a new database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()

class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test_user', password='test_password'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client, db):
    """Authentication helper fixture."""
    # Create a test user
    with client.application.app_context():
        user = User(
            username='test_user',
            password=generate_password_hash('test_password')
        )
        _db.session.add(user)
        _db.session.commit()

    return AuthActions(client)