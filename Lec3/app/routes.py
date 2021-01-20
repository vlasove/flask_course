from app import app 
from flask import render_template

# Допустим это таблица в бд
posts = [
    {
        'author' : 'Author1',
        'body' : 'Post body1',
    },
    {
        'author' : 'Author2',
        'body' : 'Post body2',
    },
    {
        'author' : 'Author3',
        'body' : 'Post body3',
    },
]

user = {
    'username' : 'Bob',
    'email' : 'bob@mail.ru',
    'age' : 33,
}

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'home.html',
        posts=posts,
        user=user,
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        user=user,
    )
