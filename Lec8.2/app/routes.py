
from app import app 
from app.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash 

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

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == '123456':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html" , posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")