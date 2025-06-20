import pytest
from app import create_app, db
from app.models import User, Article
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(username='test', password=generate_password_hash('test'))
            db.session.add(user)
            db.session.commit()
        yield client

def test_home_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login(client):
    response = client.post('/login', data={'username': 'test', 'password': 'test'}, follow_redirects=True)
    assert b'Liste des articles' in response.data
