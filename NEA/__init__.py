from flask import Flask
from .views.login import login


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.register_blueprint(login, url_prefix='/')
