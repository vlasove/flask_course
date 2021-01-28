# Лекция 13. Сброс пароля

***Задача*** реализоват ьпростейший механизм сброса пароля.

### Шаг 0. Идея
* Пользователь разлогинен.
* Переходит по ссылке ```/reset_password```
* Вводит адрес электронной почты
* Проверяем, есть ли аккаунт, связанный с этой почтой
* Если есть, нам нужна ссылка, ведущая на страницу сброса пароля
* Чтобы создать ссылку, мы закодируем id пользователя (email которого ввели ранее) в токен (у токена будет время жизни).
* Включим токен в ссылку вида ```https://loacalhost:8000/reset/24ryiy7yhf2hf24hf24f7i2f23hf23gfgg```
* Затем пользователь проходит по ссылке ```https://loacalhost:8000/reset/24ryiy7yhf2hf24hf24f7i2f23hf23gfgg```
* Затем строку раскодируем. 
* Если в резульатте декодирования получаем ```id``` валидный - то только после этого показываем форму с полями ```New Password```, ```New Password (Again)```

### Шаг 1. Как выбить токен с временем жизни?
Для этого нам понадобится модуль ```itsdangerous```  в котором живет это чудовщие 
```
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
```
```
>>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
>>> s = Serializer('secret', 20)
>>> token = s.dumps({'user_id' : 1}).decode('utf-8')
>>> token
'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxMTg1NzA5NiwiZXhwIjoxNjExODU3MTE2fQ.eyJ1c2VyX2lkIjoxfQ.vgOcG6Z843UhQMhSpTJk_RSDLlfoWKRpqe2r-EP5632bxRiY-UyVZZpZ8nmxgpIF_TcmRsWB4Zf35G1zMFnM3Q'
>>> s.loads(token)
{'user_id': 1}
>>> s.loads(token)
{'user_id': 1}
>>> s.loads(token)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "c:\users\administrator\.virtualenvs\lec13-hr_fha2x\lib\site-packages\itsdangerous\jws.py", line 202, in loads
    raise SignatureExpired(
itsdangerous.exc.SignatureExpired: Signature expired
```

### Шаг 2. Обновим модель
```
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login.user_loader
def load_user(user_id:int):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   
    
    def get_password_reset_token(self, expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(int(user_id)
        
```

### Шаг 3. Добавим 2 новые формы.
В файле ```forms.py``` создадим 2 формы:
```
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit =  SubmitField("Request for Password reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Try to register.')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit =  SubmitField("Set new password")
```

### Шаг 4. Добавим 2 новых рута
В файле ```routes.py```
```
@app.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_password_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('password_reset'))
    if request.method == 'POST' and form.validate_on_submit():
        pass 
    return render_template('password_reset_token.html', form=form)


@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = PasswordResetRequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        flash('Password reset token was sended', 'success')
        print('Sending email to:', user.email,"\n\nWith token:", user.get_password_reset_token())
        return redirect(url_for('password_reset'))
    return render_template('password_reset.html', form=form)
```

Сверстаем шаблон ```password_reset.html```
```
{% extends "base.html" %}

{% block title %}Password reset?{% endblock %}

{% block content %}
    <div class="content-section">
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Password reset?</legend>
                <div class="form-group">
                    {{ form.email.label(class="form-control-label") }}
                    {% if form.email.errors %}
                        {{ form.email(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.email.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                        {{ form.email(class="form-control form-control-lg") }}
                    {% endif %}
                </div>
            </fieldset>
            <div class="form-group">
                {{ form.submit(class="btn btn-outline-info") }}
            </div>
        </form>
    </div>
    <div class="border-top pt-3">
        <small class="text-muted">
            Need An Account? <a class="ml-2" href="{{ url_for('register') }}">Sign Up Now</a>
        </small>
    </div>
{% endblock content %}
```