from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from .models import Article
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    articles = Article.query.all()
    return render_template('dashboard.html', articles=articles)

@main.route('/article/new', methods=['GET', 'POST'])
@login_required
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db.session.add(Article(title=title, content=content))
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('article_form.html')

@main.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('article_form.html', article=article)

@main.route('/article/<int:id>/delete')
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
