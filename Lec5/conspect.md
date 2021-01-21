# Лекция 5. Промежуточная карточка и модели

***Задача***: по скольку в проекте формы ввода с набором различных полей будут использоваться регулярно, создадим промежуточный шаблон ```base_card.html```. Задача данного шаблона будет состоять в том, что он разделит зоны показывания любой веб-формы.

### Шаг 1. Реализация base_card.html
Идея состоит в том, чтобы создать промежуточный адптер-шаблон , который будет наследовать ```base.html``` и размечать зоны для вставки красивой формы.

Реализация ```templates/base_card.thml```
```
{% extends 'base.html' %}

{% block content %}
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 col-md-10 col-sm-12">
                <div class="card">
                    <div class="card-header">
                        {% block card_header %}{% endblock %}
                    </div>
                    <div class="card-body">
                        {% block card_body %}{% endblock %}
                    </div>
                    <div class="card-footer text-muted text-center">
                        {% block card_footer %}{% endblock %}
                    </div>
                </div>
            </div>
        </div>
    </div>
{% endblock %}

```

### Шаг 2. Изменим шаблон login.html
```
{% extends 'base_card.html' %}

{% block title %}Log In Page{% endblock %}


{% block card_header %}
    <h3>Log In Page</h3>
{% endblock %}


{% block card_body %}
<p>You can login via following form:</p>
    <form method="POST" action="" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}<br>
            {% for error in form.username.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}<br>
            {% for error in form.password.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </p>
        <p>
            {{ form.remember.label }} {{ form.remember() }}
        </p>
        <button type="submit" class="btn btn-outline-primary">Log In</button>
    </form>
{% endblock %}


{% block card_footer %}
    <span>
        <a href="#">Forgot password?</a> or <a href="#">Sign In</a>
    </span>
{% endblock %}
    

```

### Шаг 3. Изменим шаблон post_create.html
```
{% extends 'base_card.html' %}

{% block title %}Create New Post{% endblock %}


{% block card_header %}
    <h3>Create New Post</h3>
{% endblock %}


{% block card_body %}
    
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

{% block card_footer %}
    <span>
        Back to <a href="{{ url_for('posts_list') }}">to all posts </a>.
    </span>
{% endblock %}
```


### Шаг 4. Расширения flask для работы с моделями данных
***Модель данных (модель)*** - это набор правил, задающих схему хранения данных в каком-либо хранилище.

Для того, чтобы задать модель в ```Flask``` необходмо установить 2 базовых расширения:
* ```flask_sqlachemy``` - расширение, предоставляющее API для ORM, основанной на ```SQLAlchemy```

* ```flask_migrate``` - это расширение, предоставляет API для переноса/обновления/бекапа миграций.

Установка ```pipenv install flask-sqlalchemy flask-migrate```

### Шаг 5. Конфигурация базы данных
***Условимся***, что на этой лекции будем использовать стандартную субд (sqlite3), позднее можно будет рассмотреть как мигрировать на ```PostgreSQL``` (для этого обязательно установите клиент по ссылке (версия 10) https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

Для конфигурации субд изменим содержимое файла ```conf.py```:
```
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    # Чтобы изменения в бд не засоряли консоль
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Шаг 6. Создание сущностей
Необходимо создать объект:
* ***САМОЙ ORM***
* ***Интерфейс миграции***

Для этого в файле ```app/__init__.py```
```
from flask import Flask 
from conf import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
# Объект ORM
db = SQLAlchemy(app)
# Интерфейс миграции
migrate = Migrate(app, db)

from app import routes, models
```

И создадим файл ```app/models.py```
```
```