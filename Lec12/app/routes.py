from app.forms import LoginForm, RegistrationForm, UpdateAccountForm, PostForm
from flask import redirect, url_for, render_template, flash, request, abort
from app import app, db
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
import secrets
import os
from datetime import datetime

# Выполняется перед каждым запросом!
# Для этого декоратора не важно - залогинен ли юзер или нет.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()



@app.route('/user/<username>/info')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been successfully deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post) # В полях формы уже были данные

    if post.author != current_user:
        abort(403) # Forbidden

    if request.method == 'POST' and form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data 
        db.session.add(post)
        db.session.commit()

        flash('Post has been updated successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post_update.html', post=post, form=form)

@app.route('/post/<int:post_id>/detail')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


@app.route('/post/create', methods=['GET' , 'POST'])
@login_required
def post_create():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('post_create.html', form=form)


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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = form_picture.filename.split('.')[-1]
    picture_fn = random_hex + '.' +  f_ext
    picture_path = os.path.join(app.root_path, 'static/media', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)
    if request.method == 'POST' and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username =form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    image_file = url_for('static', filename='media/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@app.route("/")
@app.route("/home")
def home():
    #http://localhost:8000/home?page=2
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html" , posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")