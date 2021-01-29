from app import mail 
from flask import url_for
import secrets
import os
from app import app
from flask_mail import Message

def reset_email_sender(user):
    # генерируем токен для пользователя user
    token = user.get_password_reset_token()
    msg = Message(
        'Password Reset Request E-Mail',
        sender='noreply@localhost.com',
        recipients = [user.email],
    )
    msg.body =f"""
    To reset your password user the following link: {url_for('users.password_reset_token', token=token, _external=True)}
    

    If you did not make this request - ignore this message.

    Regards, @localhost team!
    """

    mail.send(msg)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_ext = form_picture.filename.split('.')[-1]
    picture_fn = random_hex + '.' +  f_ext
    picture_path = os.path.join(app.root_path, 'static/media', picture_fn)
    form_picture.save(picture_path)

    return picture_fn