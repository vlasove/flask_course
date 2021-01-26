from app.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from flask import redirect, url_for, render_template, flash, request
from app import app, db
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
import secrets
import os

posts = [
    {
        'author': 'Evgeny Vlasov',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Jan 26, 2021'
    },
    {
        'author': 'John Brown',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Jan 26, 2021'
    }
]

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', form=form)

def save_picture(form_picture):
    # Есть одна большая проблема.
    # Многие медиа-файлы имеют одинаковое название
    # Решение данной проблемы заключается в следующем:
    # Генерируем 8-15 случайных символов. Прилепливаем к ним расширение медиа-файла.
    random_hex = secrets.token_hex(8) 
    file_ext = form_picture.filename.split('.')[-1]
    picture_filename = random_hex + "." +  file_ext
    picture_path = os.path.join(app.root_path, 'static/media/' , picture_filename)
    # C:/Users/Desktop/flask2/Lec9/ + static/media/ + iudgy1dg32dg1387dg3.png
    form_picture.save(picture_path)

    return picture_filename



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Your account info successfully updated!', 'success')
        return redirect(url_for('account'))

    image_file = url_for('static', filename='media/' + current_user.image_file) #static/media/default.png
    return render_template("account.html", image_file=image_file, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method =='POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login credetials", 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f'Successfully logged-in as { user.username }', 'success')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template("login.html", form=form)



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html" , posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")