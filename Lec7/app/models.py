"""
Здесь будут описываться все модели проекта
"""
from app import db ,login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id:int):
    """
    Возвращает пользователя с id
    """
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Как из User узнать, какие посты с ним ассоциированы?
    # Условно выглядеть будет так
    # new_post = Post(........)
    # new_post.author -> вернет User, ассоциированного с этим постом
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User [username={self.username}, email={self.email}]>'


    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(250))
    created =  db.Column(db.DateTime, index=True, default=datetime.now)
    # Поле связи с моделью User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post [title={self.title}, body={self.body}]>'