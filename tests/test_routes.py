import pytest
from flask import session, g
from werkzeug.security import generate_password_hash

def test_register(client, app):
    # Test GET request
    response = client.get('/auth/register')
    assert response.status_code == 200

    # Test successful registration
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.headers["Location"] == "/auth/login"

    # Verify user was added to database
    with app.app_context():
        assert User.query.filter_by(username='testuser').first() is not None

    # Test duplicate registration
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert b'already registered' in response.data

def test_login(client, app):
    # Create test user
    with app.app_context():
        user = User('testuser', generate_password_hash('testpass123'))
        db.session.add(user)
        db.session.commit()

    # Test GET request
    response = client.get('/auth/login')
    assert response.status_code == 200

    # Test successful login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.headers["Location"] == "/todo_views/index"
    assert session['user_id'] == 1

    # Test incorrect username
    response = client.post('/auth/login', data={
        'username': 'wronguser',
        'password': 'testpass123'
    })
    assert b'Incorrect username' in response.data

    # Test incorrect password
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert b'Incorrect password' in response.data

def test_logout(client, auth):
    auth.login()

    response = client.get('/auth/logout')
    assert response.headers["Location"] == "/"

    assert 'user_id' not in session

def test_login_required(client, auth):
    # Test accessing protected route without login
    response = client.get('/protected-route')
    assert response.headers["Location"] == "/auth/login"

    # Login and test again
    auth.login()
    response = client.get('/protected-route')
    assert response.status_code == 200

def test_load_logged_in_user(client, auth):
    # Test with no login
    with client:
        client.get('/')
        assert g.user is None

    # Test with login
    auth.login()
    with client:
        client.get('/')
        assert g.user is not None
        assert g.user.username == 'testuser'