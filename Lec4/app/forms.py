from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    author = StringField("Author Name" , validators=[DataRequired()])
    body = StringField("Post content", validators=[DataRequired()]) 
    submit = SubmitField('Create Post')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =  BooleanField('Remember me?')
    submit = SubmitField('Log In')

