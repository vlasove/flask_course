from app.forms import LoginForm, RegistrationForm, UpdateAccountForm
from flask import redirect, url_for, render_template, flash, request
from app import app, db
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

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


@app.route('/account')
@login_required
def account():
    form = UpdateAccountForm()
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