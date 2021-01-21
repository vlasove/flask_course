from flask import Flask 
from conf import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
# Объект ORM
db = SQLAlchemy(app)
# Интерфейс миграции
migrate = Migrate(app, db)
# интерфейс login
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

