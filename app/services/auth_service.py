from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from app.models import User

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return True
    return False

def perform_logout():
    logout_user()