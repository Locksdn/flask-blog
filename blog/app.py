from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flaskext.markdown import Markdown

app = Flask(__name__)

app.config['SECRET_KEY'] = 'themostsecretkeyintheworld'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

Markdown(app, safe_mode=True)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from . import api

from .views import views
app.register_blueprint(views)

from .admin import admin
app.register_blueprint(admin)