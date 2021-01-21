# Лекция 6. Модели и аккаунтинг

***Задача*** создать базовые модели Post и User, а также натсроить функционал:
```
/login
/logout
/register
```

### Шаг 1. Реализация пользовательской модели
В файле ```app/models.py```
```
"""
Здесь будут описываться все модели проекта
"""
from app import db 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User [username={self.username}, email={self.email}]>'  
```

Теперь откроем командную строку и выполним следующий запрос:
```
>>> from app.models import User
>>> u = User(username='bob', first_name='Bobby', second_name='Brown', email='bob@gmail.com')
>>> u
```

### Шаг 2. Инициализация миграционного репозитория
***Миграционный репозиторий*** - это место, где будут храниться версии схем базы данных для данного проекта.

Для того, чтобы проинициализировать данный репозиторий выполним команду
```
flask db init
```

### Шаг 3. Подготовка миграции
Для того, чтобы сгенерировать запросы на изменение схемы хранения данных, необходимо выполнить команду:
```
flask db migrate -m "user initial table"
```

### Шаг 4. Применение миграции
Для того, чтобы сгенерированные запросы применились к бд, необходмо ***применить*** миграцию.
Выполняется это командой 
```
flask db upgrade
```

### Шаг 5. Создание модели поста
Опишем модель ```Post``` (```app/models.py```)
```
"""
Здесь будут описываться все модели проекта
"""
from app import db 
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Как из User узнать, какие посты с ним ассоциированы?
    # Условно выглядеть будет так
    # new_post = Post(........)
    # new_post.author -> вернет User, ассоциированного с этим постом
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User [username={self.username}, email={self.email}]>'  

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(250))
    created =  db.Column(db.DateTime, index=True, default=datetime.now)
    # Поле связи с моделью User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post [title={self.title}, body={self.body}]>'
```

Поскольку сейчас были созданы новые схемы хранения (или изменены старые), необходимо опят ьподготовить миграционный скрипт и применить его к базе данных.
```
flask db migrate 
flask db upgrade
```

### Шаг 6. Проверим, что все получилось так, как ожидалось
Откроем консоль и создадим первого пользователя:
```
>>> from app.models import User, Post
>>> u = User(username='bob', first_name='Bobby', second_name='Brown', email='bob@gmail.com')
>>> u
<User [username=bob, email=bob@gmail.com]>
>>> from app import db
>>> db.session.add(u)
>>> db.session.commit()
>>>

```

Получение всех объектов модели
```
User.query.all()
```

Поулчение объекта по ```ID```
```
User.query.get(1)
```

Создадим пост привязанный к ```bob```
```
>>> bob = User.query.get(1)
>>> post = Post(title="Simple title", body="Simple body", author=bob)
>>> db.session.add(post)
>>> db.session.commit()
>>> posts = Post.query.all()
>>> posts
[<Post [title=Simple title, body=Simple body]>]
>>> posts[0].author
<User [username=bob, email=bob@gmail.com]>
```

### Шаг 7. Контекст командной оболочки
В прошлом примере - необходимо каждый запуск подгружать (импортировать) зависимости проекта, этого можно избежать если определить ```shell_context```

Зайдем в файл ```main.py```
```
from app import app, db 
from app.models import User, Post 


@app.shell_context_processor
def make_shell_context():
    return {
        'db' : db, 
        'app' : app, 
        'Post' : Post,
        'User' : User,
    }


```

Теперь консоль будет открывать командой ```flask shell```.


### Шаг 8. Как создавать password_hash?
```
>> from werkzeug.security import generate_password_hash
>>> password = "HelloKitty"
>>> hash = generate_password_hash(password)
>>> hash
'pbkdf2:sha256:150000$MufMeFTA$b1fa2d8c3ef3a89ad7a4e6f9aa9ad46e9836482a43a070a928cd43c0b0c1a672'
>>> from werkzeug.security import check_password_hash
>>> check_password_hash(hash, "HelloKitty")
True
>>> check_password_hash(hash, "HelloKittyAndDog")
False
```

Теперь добавим эту логику к модели
```
# app/models.py
"""
Здесь будут описываться все модели проекта
"""
from app import db 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # Как из User узнать, какие посты с ним ассоциированы?
    # Условно выглядеть будет так
    # new_post = Post(........)
    # new_post.author -> вернет User, ассоциированного с этим постом
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User [username={self.username}, email={self.email}]>'


    def set_password(self, password):
        self.password_hash = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   
```


### Шаг 9. Реализация ```login``` функционала
Для начала установим расширение ```flask_login``` 
```
pipenv install flask_login
```

После этого в ```app?__init__.py``` определим объект
```
from flask import Flask 
from conf import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
# Объект ORM
db = SQLAlchemy(app)
# Интерфейс миграции
migrate = Migrate(app, db)
# интерфейс login
login = LoginManager(app)

from app import routes, models

```

### Что приносит flask_login?
Во-первых, данное расширение приносит батарейку, которая позволяет добавлять к объектам (выполняющих роль пользователя), такие поля:
* ```is_authenticated```
* ```is_active```
* ```is_anonymous```

Данные поля мы виртуально встроим в ```User```
```
from flask_login import UserMixin

class User(UserMixin, db.Model):
    ....
```

В виду особеностей реализации расширения flask-login нам (как разработчикам) необходимо реализовать ```id``` загрузчик для объектов пользовательской модели.
```
from app import db, login 
....

@login.user_loader
def load_user(id:int):
    """
    Возвращает пользователя с id
    """
    return User.query.get(int(id))
```

### Шаг 10. Реализация routes
```app/routes.py```
```
from flask_login import current_user, login_user, logout_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts_list'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password_hash(form.password.data):
            flash("Invalid login credetials")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f'Successfully logged-in as { user.username }')
        return redirect(url_for('posts_list'))
        
    return render_template(
        'login.html',
        form=form,
    )
```

### Шаг 11. Как закрыть доступ незалогиненому пользователю к страницам?
Для реализации механизма ```login_required``` необходимо
* Определить место, куда отправлять логиниться
```
# app/__init__.py
login = LoginManager(app)
login.login_view = 'login'
```

* Завернуть декоратором те функции, которые вам необходимы:
```
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/posts/create', methods=['GET', 'POST'])
@login_required
def post_create():
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
        return redirect(url_for('posts_list'))

    return render_template(
        'post_create.html',
        form=form,
    )

@app.route('/posts')
@login_required
def posts_list():
    return render_template(
        'posts_list.html',
        posts=posts,
        user=user,
    )

```

* Важно помнить, что после того, как юзер будет перенаправлен на ```login``` его нужно будет вернуть назад. ```/login?next=/post_list```
Для того, чтобы обработать ```next``` необходимо в функции login добавить следующее:
```
from werkzeug.urls import url_parse

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts_list'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid login credetials")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        flash(f'Successfully logged-in as { user.username }')
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('posts_list')
        return redirect(next_page)
        
    return render_template(
        'login.html',
        form=form,
    )
```