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


### Шаг 5. Подключение модели Post к проекту.
В файле ```app/routes.py```
```
@app.route('/posts')
@login_required
def posts_list():
    posts = Post.query.all()
    return render_template(
        'posts_list.html',
        posts=posts,
    )
```

В шаблоне же внесем следующие изменения:
```
{% extends 'base.html' %}

{% block title %}All Posts{% endblock %}

{% block content %}
    {% for post in posts %}
        <div class="card">
            <div class="card-header text-muted">
                {{ post.author.username }} writes at {{ post.created }}
            </div>
                
            <div class="card-body">
                <h3> {{ post.title }} </h3>
                <p> {{ post.body }} </p>
            </div>

            <div class="card-footer text-muted text-center">
                <a href="#">Edit</a> | <a href="#">Delete</a>
            </div>
        </div>
        <br>
    {% endfor %}

{% endblock %}
```

### Шаг 6. Создание нового поста
Поскольку в преокте используется расширение ```flask-login``` (которое предоставляет нам объект ```current_user```), потребность в поле формы ```PostForm.author``` пропала. Будем определять автора поста исходя из того, кто сейчас его создает.
Для этого внесем изменение в форму ```PostForm```:
```
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField("Post content", validators=[DataRequired()]) 
    submit = SubmitField('Create Post')
```

После чего изменим правило отображения формы в шаблоне (удалив блок, связанный с показом поля ```author```).

И также необходимо изменить логику создания поста:
```
@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def post_create():
    
    form = PostForm()
    if request.method == 'POST' and form.validate():
        new_post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Post successfully created!')
        return redirect(url_for('posts_list'))

    return render_template(
        'post_create.html',
        form=form,
    )
```

### Шаг 7. Реализация детального просмотра для каждого поста
Первым делом создадим функцию ```post_detail```
```
@app.route('/posts/<id>/', methods=['GET'])
@login_required
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template(
        'post_detail.html',
        post=post,
    )
```

Обратим внимание на то, что данная ссылка является динамической (в ней присутсвуют параметры) с ```<id>``` . ```@app.route(...)``` работает так, что он парсит динамические параметры и передает их на вход функциям, которые декарируются через ```@app.route(...)```.

После этого создадим шаблон для отображения конкретного поста ```post-detail.html```
```
{% extends 'base_card.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block card_header %}
    <h3>{{ post.title }}</h3>
{% endblock %}

{% block card_body %}
    <p>
        <b>{{ post.author.username }}</b> create at {{ post.created }}
    </p> <hr>
    <p>
        {{ post.body }}
    </p>
{% endblock %}

{% block card_footer %}
    <small>
        <a href="#">Edit</a> | <a href="#">Delete</a>
    </small>
{% endblock %}
```

И в ```posts_list.html``` добавим следующую ссылку :
```
<a href="{{ url_for('post_detail', id=post.id) }}">To detail view</a>
```