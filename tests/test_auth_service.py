import pytest
from app.models import User
from services.auth_service import authenticate_user, perform_logout

def test_authenticate_user_success(mocker, client):
    user = User(username='test')
    user.set_password('test123')
    mocker.patch('app.models.User.query.filter_by', return_value=mocker.Mock(first=lambda: user))
    mocker.patch('services.auth_service.check_password_hash', return_value=True)
    mocker.patch('services.auth_service.login_user')
    assert authenticate_user('test', 'test123') is True

def test_authenticate_user_failure(mocker):
    mocker.patch('app.models.User.query.filter_by', return_value=mocker.Mock(first=lambda: None))
    assert authenticate_user('wrong', 'wrong') is False

def test_perform_logout(mocker):
    mock_logout = mocker.patch('services.auth_service.logout_user')
    perform_logout()
    mock_logout.assert_called_once()