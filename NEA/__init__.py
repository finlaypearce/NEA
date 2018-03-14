from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .views.login import login
from NEA import models

app.register_blueprint(login, url_prefix='/')
