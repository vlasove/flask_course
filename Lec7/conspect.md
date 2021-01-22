# Лекция 7. Пользовательская регистрация

***Задача*** : научиться регестрировать пользователя не через консоль (flask shell), а через интерфейс на веб-страницах.

### Шаг 1. Определение формы (определение интерфейса)

В файле ```app/forms.py```
```
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

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
```

***Важно***, что валидатор ```Email``` по умолчанию отсутствует в ```flask_wtf``` , поэтому добавим в проект расширение ```pipenv install email-validator```.

Методы, название которых начинается с фразы ```validate_``` отрабатывают на этапе валидации формы в следующем порядке:
* В общем коде видим ```form.validate()```
* После этого запускаются валидаторы, явно указанные в полях формы ```DataReuired(), Email(), EqualTo(),....```
* После этого запускаются пользовательские валидаторы (названия обязаны начинаться c ```validate_....```)


### Шаг 2. Определение url и route
В файле ```routes.py``` определим следующую функцию
```
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts_list'))
    form = UserRegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Congrats. Account successfully created.')
        return redirect(url_for('login'))
    return render_template(
        'register_form.html',
        form=form,
    )
```


### Шаг 3. Создание шаблона
Создадим файл ```app/templates/register_form.html```
```
{% extends 'base_card.html' %}

{% block title %}New User Registration{% endblock %}


{% block card_header %}
    <h3>New User Registration</h3>
{% endblock %}

{% block card_body %}
    <p>You can register using following form:</p>
    <form action="" method="POST" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32)}}<br>
            {% for error in form.username.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.first_name.label }}<br>
            {{ form.first_name(size=32)}}<br>
            {% for error in form.first_name.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.second_name.label }}<br>
            {{ form.second_name(size=32)}}<br>
            {% for error in form.second_name.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.email.label }}<br>
            {{ form.email(size=32)}}<br>
            {% for error in form.email.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32)}}<br>
            {% for error in form.password.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password2.label }}<br>
            {{ form.password2(size=32)}}<br>
            {% for error in form.password2.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>

        <button type="submit" class="btn btn-outline-primary">Register</button>
    </form>
{% endblock %}

{% block card_footer %}
    <span>
        Already have an account? Try to <a href="{{ url_for('login') }}">log in</a> .
    </span>
{% endblock %}
```

### Шаг 4. Добавим регистрацию в base-шаблон
```
                {% if not current_user.is_authenticated %}
                    <li class="nav-item">
                    <a class="nav-link active" href="{{ url_for('register') }}">Register</a>
                    </li>
                {% endif %}
```

Теперь в случае, если пользователь не залогинен, будут выводиться 2 дополнительных поля (```login```, ```register```). А в случае, если пользователь залогинен - будет видно только 1 поле (```logout```).