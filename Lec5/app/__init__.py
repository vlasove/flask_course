from flask import Flask 
from conf import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
# Объект ORM
db = SQLAlchemy(app)
# Интерфейс миграции
migrate = Migrate(app, db)

from app import routes, models

