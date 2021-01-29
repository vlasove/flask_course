from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from datetime import datetime

"""
Для интеграции api
"""
# from flask_restful import Api
# from app.api.resources import Resource1, Resource2, Resource3


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
# api = Api(app)


login = LoginManager(app)
login.login_view = 'users.login'
login.login_message_category = 'info'

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main 


app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

"""
Добавление части api
"""
#api.add_resource(Resource1, "api/resource1")
#api.add_resource(Resource2, "api/resource2")
#api.add_resource(Resource3, "api/resource3")


from app import models
