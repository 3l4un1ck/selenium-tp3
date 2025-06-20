from app import app

def test_home_redirect():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 302

def test_login_success():
    with app.test_client() as client:
        response = client.post('/login', data={'username': 'admin', 'password': 'admin'}, follow_redirects=True)
        assert b'Contacts' in response.data