# Лекция 4. Добавление веб-форм

***Задача***: добавить простейшие веб-формы, имитирующие пользовательский ```login``` и добавление нового объекта  список ```posts```.


### Шаг 1. Конфигурация расширения flask-wtf
```flask-wtf``` - это расширение фреймворка ```flask```, позволяющее работать (обрабатывать) поля веб-форм (flask-WebTemplateForm).
Для установки расширения выполним 2 действия:
* ```pipenv install flask-wtf```
* Необходимо отконфигурировать формы, а именно ввести конфиг ```SECRET_KEY```

#### Конфигурация ```SECRET_KEY```
* Самый простой способ - это включить следующую строчку в ```app/__init__.py```
```
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySuperSecretKeyForThisApplication12683156721r34'

from app import routes
```
Но данный способ заставляет хардкодить ключ приложения прямо в исходнике (абсолютно небезопасно).

* Второй способ - чуть хитрее - поместить SECRET_KEY в ```.env```
```
from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

* Третий способ - это наиболее предпочтителен в Flask сообществе - это создадние ```conf.py``` файла и конфигурация через ***классы***.

Для этого создадим файл ```conf.py``` в корне проекта:
```
import os 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
```

Удобство состоит в том, что все необходимые сторонние конфигуративные требования будут изложены в отдельном модуле (в случае необходимости - данный модуль можно заменить).

Теперь в файле ```app/__init__.py``` заменим конфигурацию через создание объекта:
```
app.config.from_object(Config)
```

### Шаг 2. Создание форм.
Стандартно формы хранятся внутри модуля ```forms.py``` (расположим его в ```app/forms.py```)
```
from flask_wtf import FlaskForm
from wtforms import StringFiled, PasswordField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    author = StringFiled("Author Name" , validators=[DataRequired()])
    body = StringFiled("Post content", validators=[DataRequired()]) 
    submit = SubmitField('Create Post')

```

После того, как реализовали форму, необходимо прописать, когда ее показываем и каким запросом обрабатываемю

Для этого внутри ```app/routes.py```
```
from app.forms import PostForm


@app.route('/create')
def create_post():
    form = PostForm()
    return render_template(
        'create.html',
        form=form,
    )

```

Добавим ссылку на эту страницу в ```base.html```
```
        <!--Добавление простейшей панели навигации -->
        <div>
            MyAppName : <a href="{{ url_for('home') }}">Home</a> 
            |
            <a href="{{ url_for('about') }}">About</a>
            |
            <a href="{{ url_for('create_post')}}">+NewPost</a>
        </div>
```

После этого реализуем логику работы функции ```create_post```
```
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate():
        new_post_author = form.author.data
        new_post_body = form.body.data

        new_post = {
            'author' : new_post_author,
            'body' : new_post_body,
        } 
        posts.append(new_post)
        return redirect(url_for('home'))

    return render_template(
        'create.html',
        form=form,
    )

```


### Шаг 3. Флешки
```flash```- уведомления достаточно полезны, позволяет информаировать клиента о каких-либо проишествиях (success, error, abort) 
Добавим в наш проект флешки, которые будут отображать, что пост был создан успешно.
Для этого в ```app/routes.py```
```
from flask import flash 

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate():
        new_post_author = form.author.data
        new_post_body = form.body.data

        new_post = {
            'author' : new_post_author,
            'body' : new_post_body,
        } 
        posts.append(new_post)
        flash('Post successfully created!')
        return redirect(url_for('home'))

    return render_template(
        'create.html',
        form=form,
    )

```

Для того, чтобы поймать флеш-уведомление из шаблона , существует специальная функция , которая называется ```get_flashed_messages()```.
```
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul>
                    {% for message in messages %}
                        <ul>{{ message }} </ul>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
```

Первичный вызов ```get_flashed_messages()``` опустошает очередь всех ```flash``` уведомлений и возвращает список. То есть если мы вызовем ее повторно, но никаких уведомлений она уже не вернет. Для этого вводим переменную ```messages``` при помощи блока
```
{% with messages = ... %}
    ....
{% endwith %}
```
Внутри ```with``` блока будет создана переменная ```messages``` и видна всем в этом блоке

### Шаг 4. Показ валидационных сообщений
В нашей форме имеются валидаторы ```DataRequired()``` и данные валидаторы в случае возникновения ошибки возвращают наборы ```errors```, теперь мы хотим эти наборы отразить в шаблонах форм (```app/templates/create.html```)
```
{% extends 'base.html' %}

{% block title %}Create New Post{% endblock %}

{% block content %}
    <h1>Create New Post</h1>
    <form action="" method="POST" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.author.label }}<br>
            {{ form.author(size=40)}}<br>
            {% for error in form.author.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.body.label }}<br>
            {{ form.body(size=60)}}<br>
            {% for error in form.body.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <!-- {{ form.submit() }}
        <input type="submit" value="Create"> -->
        <button type="submit" class="btn btn-outline-primary">Create Post</button>
    </form>
{% endblock %}
```

***novalidate*** - данное поле в html форме означает, что вы не собираетесь просить браузер провести валидацию полей своим стандартным способом.Вместо этого вы проводите валидацию на стороне сервера.

### Шаг 5. Имитация логина пользователя
На данный момент информация про текущего пользователя хранится не в сессии, а в ```runtime``` приложения в виде обычного словаря. 
Хотим сделать так, чтобы при выполнении операции ```login``` имя (username) текущего пользователя подменялся на тот, который был указан в веб-форме.
Для этого, создадим форму:
```
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =  BooleanField('Remember me?')
    submit = SubmitField('Log In')
```

Обратим внимание на то, что данная форма не привязана ни к чему (ни какой модели с ней не ассоциировано).

После создания формы(интерфейс взаимодействия), создадим route:
```
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        new_username = form.username.data 
        user['username'] = new_username 
        flash(f'Successfully logged-in as {new_username}')
        return redirect(url_for('home'))
        
    return render_template(
        'login.html',
        form=form,
    )

```
Функция ```login``` способна обрабатывать запросы двух типов:
* Если это запрос типа ```GET``` - то данная функция просто рисует форму и все
* Если жто запрос ```POST``` (провоцируется нажатим "submit" ) то, сначала проводится инвалидация формы (form.validate()) , а после чего мы извлекаем из фомры данные и обновляем ```username``` в словаре ```user```, попутно выбрасываем флешку и перенаправляем пользователя на домашнюю страницу.