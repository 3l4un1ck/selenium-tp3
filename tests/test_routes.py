import pytest

from app import create_app, db
from app.models import User, Article
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Create a test client
    with app.test_client() as testing_client:
        # Establish application context
        with app.app_context():
            # Create all database tables
            db.create_all()
            yield testing_client
            # Clean up after a test
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='function')
def init_database(test_client):

    # Create a test user
    test_user = User(username='test')
    test_user.set_password('test123')

    # Add to a database
    db.session.add(test_user)
    db.session.commit()

    yield  # this is where the testing happens

    # Cleanup (will be done automatically by test_client fixture)


def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200

def test_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check that the response is valid
    """
    response = test_client.post('/login',
                              data=dict(username='test', password='test123'),
                              follow_redirects=True)
    assert response.status_code == 200
