from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Contact
import os

app = Flask(__name__)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    contact = Contact(name=name, email=email)
    db.session.add(contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.email = request.form['email']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)