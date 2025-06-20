from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    username = input("Nom d'utilisateur : ")
    password = input("Mot de passe : ")
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    print("Utilisateur créé avec succès !")
