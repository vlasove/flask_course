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

@app.route('/posts')
def posts_list():
    return render_template(
        'posts_list.html',
        posts=posts,
        user=user,
    )

@app.route('/')
def homepage():
    return render_template('home.html')

