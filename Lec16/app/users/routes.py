from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm, UpdateAccountForm,  PasswordResetRequestForm, PasswordResetForm
from app import db 
from app.models import User, Post 
from werkzeug.urls import url_parse
from .utils import save_picture, reset_email_sender


users = Blueprint('users', __name__)

@users.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_password_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.password_reset'))
    form = PasswordResetForm()
    if request.method == 'POST' and form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password was set. Try to lgin.', 'success')
        return redirect(url_for('users.login')) 
    return render_template('password_reset_token.html', form=form)


@users.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = PasswordResetRequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        reset_email_sender(user)
        flash('Password reset token was sended to your email. Check inbox:)', 'info')
        return redirect(url_for('users.login'))
    return render_template('password_reset.html', form=form)


@users.route('/user/<username>/info')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if request.method =='POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login credetials", 'danger')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember.data)
        flash(f'Successfully logged-in as { user.username }', 'success')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('main.home')
        return redirect(next_page)
    return render_template("login.html", form=form)


@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    image_file = url_for('static', filename='media/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)
