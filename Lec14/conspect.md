# Лекция 13. Сброс пароля (продолжение)

### Шаг 1. Допишем шаблон для reset_token
Создадим шаблон ```app/templates/password_reset_token.html```

```
{% extends 'base.html' %}

{% block title %}Password Reset Page{% endblock %}

{% block content %}

    <div class="content-section">
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Reset you password</legend>
                <div class="form-group">
                    {{ form.password.label(class="form-control-label") }}
                    {% if form.password.errors %}
                        {{ form.password(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.password.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                        {{ form.password(class="form-control form-control-lg") }}
                    {% endif %}
                </div>
                <div class="form-group">
                    {{ form.confirm_password.label(class="form-control-label") }}
                    {% if form.confirm_password.errors %}
                        {{ form.confirm_password(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.confirm_password.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                        {{ form.confirm_password(class="form-control form-control-lg") }}
                    {% endif %}
                </div>
            </fieldset>
            <div class="form-group">
                {{ form.submit(class="btn btn-outline-info") }}
            </div>
        </form>
    </div>
{% endblock %}
```

Посмотрим как это выглядит.

### Шаг 2. Реализация механизма сброса пароля

* Незалогинненный пользователь приходит по ссылке ```/password_reset``` (+)
* Вводит почту (+)
* Если пользователя с такой почтой в БД нет - то ничего не делаем (выведем флеш уведомление о том, что такого нет) (+)
* Если такой есть - то мы пробиваем этому пользователю токен с временем жизни 1 час (например token 17dfs1672sf12)
* После этого собираем ссылку вида ```http://localhost:8000/password_reset/17dfs1672sf12```
* Данную ссылку отправляем по почте пользователю
* Затем пользователь проходит по этой ссылке и попадает на страницу ```/password_reset/<token>```.
* Проверяем что такое не стух
* Раскодиуем токен (извлекаем словарь {'user_id' : id })
* И для пользователя с ```id``` выдаем форму с двумя полями для ввода пароля.
* После этого устанавливаем пароль и отправляем на страницу ```login```

#### Подключение электронной почты
* Для работы с почтовыми службами в ```flask``` имеется расширение ```flask-mail```:
```pipenv install flask-mail```

* Инициализация объекта почты (```app?__init__.py```)
```
from flask_mail import Mail
mail = Mail(app)
```
* Конфигурация для объекта ```Mail``` заходим в ```config.py``` (требуется наличие ```gmail``` аккаунта)
```
class Config:
    ....
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('USER_EMAIL_ADDRESS') # ваш адрес электронной почты
    MAIL_PASSWORD = os.environ.get('USER_EMAIL_PASSWORD') # ваш пароль от электронной почты
```

* В файле ```.env``` добавим:
```
USER_EMAIL_ADDRESS = 'vasya@gmail.com'
USER_EMAIL_PASSWORD = '123213725'
```

#### Опишем функцию reset_email_sender
```
from app import mail
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
    To reset your password user the following link: {url_for('password_reset_token', token=token, _external=True)}
    

    If you did not make this request - ignore this message.

    Regards, @localhost team!
    """

    mail.send(msg)
```

***Важно*** в ```development``` режиме все сообщения дублируются в консоль.


Поправим функцию ```password_reset_token```:
```
@app.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_password_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('password_reset'))
    form = PasswordResetForm()
    if request.method == 'POST' and form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password was set. Try to lgin.', 'success')
        return redirect(url_for('login')) 
    return render_template('password_reset_token.html', form=form)

```

Зайдем в шаблон ```login.html```
```
href= "{{ url_for('password_reset') }}"
```

Проверим что все работает.


***P.S.*** данный способ сброса пароля на данный момент - самый логичный.
***Как не надо делать***:
* когда пользователь жмет на password_reset - ему в бд уже пишется какой-то стандартный пароль
* когда пользователь жмет на password_reset - ему в бд добавляется случайный пароль