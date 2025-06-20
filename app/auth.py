from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from .models import User
from . import db, login_manager
from .services import auth_service

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if auth_service.authenticate_user(username, password):
            return redirect(url_for('main.dashboard'))
        flash('Identifiants invalides')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    auth_service.perform_logout()
    return redirect(url_for('auth.login'))
