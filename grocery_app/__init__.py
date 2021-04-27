from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from grocery_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)


db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
bcrypt = Bcrypt(app)

from grocery_app.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from grocery_app.auth.routes import auth
from grocery_app.main.routes import main

app.register_blueprint(main)
app.register_blueprint(auth)


with app.app_context():
    db.create_all()
