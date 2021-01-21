from app import app 
from flask import render_template, request, flash, redirect, url_for
from app.forms import PostForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse


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
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts_list'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login credetials")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f'Successfully logged-in as { user.username }')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('posts_list')
        return redirect(next_page)
        
    return render_template(
        'login.html',
        form=form,
    )

@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def post_create():
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
        return redirect(url_for('posts_list'))

    return render_template(
        'post_create.html',
        form=form,
    )

@app.route('/posts')
@login_required
def posts_list():
    return render_template(
        'posts_list.html',
        posts=posts,
        user=user,
    )

@app.route('/')
def homepage():
    return render_template('home.html')

