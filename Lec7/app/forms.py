from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User 



class UserRegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    first_name = StringField(label='First Name', description="Can be blank")
    second_name = StringField(label='Second Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password2 = PasswordField(
        label='Repeat password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(label='Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("User with that username already exists.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("User with that email address already exists.")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField("Post content", validators=[DataRequired()]) 
    submit = SubmitField('Create Post')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =  BooleanField('Remember me?')
    submit = SubmitField('Log In')
