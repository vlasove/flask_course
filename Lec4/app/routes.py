from app import app 
from flask import render_template, request, redirect, url_for, flash
from app.forms import PostForm, LoginForm

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        new_username = form.username.data 
        user['username'] = new_username 
        flash(f'Successfully logged-in as {new_username}')
        return redirect(url_for('home'))
        
    return render_template(
        'login.html',
        form=form,
    )

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate():
        new_post_author = form.author.data
        new_post_body = form.body.data

        new_post = {
            'author' : new_post_author,
            'body' : new_post_body,
        } 
        posts.append(new_post)
        flash('Post successfully created!')
        return redirect(url_for('home'))

    return render_template(
        'create.html',
        form=form,
    )


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
