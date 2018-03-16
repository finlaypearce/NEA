from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login.loginform'

from .views.login import login
from .views.student import student
from .views.profile import profile
from NEA import models
from .models import User


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()


app.register_blueprint(login)
app.register_blueprint(student, url_prefix='/student')
app.register_blueprint(profile, url_prefix='/user')
