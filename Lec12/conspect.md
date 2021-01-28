# Лекция 12. Пагинация

### Шаг 1. Что такое SqlAlchemy.Paginate?
В ```flask-sqlalchemy``` уже встроен необходимый объект, для разбиения контента на несколько страниц.
Пример простейшей работы - ниже:

```
>>> posts = Post.query.paginate()
>>> posts
<flask_sqlalchemy.Pagination object at 0x0000016A079E4E50>
>>> dir(posts)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'has_next', 'has_prev', 'items', 'iter_pages', 'next', 'next_num', 'page', 'pages', 'per_page', 'prev', 'prev_num', 'query', 'total']
>>> posts.per_page
20
>>> posts.page
1
>>> posts.items
[Post('Second post by admin [UPDATED]', '2021-01-28 18:57:35.325491'), Post('Another admin [UPDATED]', '2021-01-28 19:28:57.022207'), Post('Post by TestUser', '2021-01-28 19:29:39.495449'), Post('Another [UPDATED]', '2021-01-28 19:30:41.190025'), Post('Post by superCoder', '2021-01-28 19:34:00.998118'), Post('Another Post from web form', '2021-01-28 19:34:05.515325'), Post('asdasdasdasd', '2021-01-28 19:34:09.460515'), Post('asdsdf12e1dd21', '2021-01-28 19:34:22.331257'), Post('adasxzvcqc', '2021-01-28 19:34:27.483240'), Post('ads121d21d1', '2021-01-28 19:34:38.740324'), Post('adsaads', '2021-01-28 19:34:42.881518')]
>>> for post in posts.items:
...     print(post)
...
Post('Second post by admin [UPDATED]', '2021-01-28 18:57:35.325491')
Post('Another admin [UPDATED]', '2021-01-28 19:28:57.022207')
Post('Post by TestUser', '2021-01-28 19:29:39.495449')
Post('Another [UPDATED]', '2021-01-28 19:30:41.190025')
Post('Post by superCoder', '2021-01-28 19:34:00.998118')
Post('Another Post from web form', '2021-01-28 19:34:05.515325')
Post('asdasdasdasd', '2021-01-28 19:34:09.460515')
Post('asdsdf12e1dd21', '2021-01-28 19:34:22.331257')
Post('adasxzvcqc', '2021-01-28 19:34:27.483240')
Post('ads121d21d1', '2021-01-28 19:34:38.740324')
Post('adsaads', '2021-01-28 19:34:42.881518')
>>>
```

Как можно его конфигурировать?
```
>>> posts = Post.query.paginate(per_page = 3)
>>> posts.page
1
>>> posts.items
[Post('Second post by admin [UPDATED]', '2021-01-28 18:57:35.325491'), Post('Another admin [UPDATED]', '2021-01-28 19:28:57.022207'), Post('Post by TestUser', '2021-01-28 19:29:39.495449')]
>>> posts = Post.query.paginate(page=2, per_page=3)
>>> posts.items
[Post('Another [UPDATED]', '2021-01-28 19:30:41.190025'), Post('Post by superCoder', '2021-01-28 19:34:00.998118'), Post('Another Post from web form', '2021-01-28 19:34:05.515325')]
>>> posts.total
11
>>>
```
Объект ```Paginate``` имеет 2 интересных для нас параметра:
* ```page``` - номер страницы
* ```per_page``` - сколько объектов будет отображено на одной странице.

### Шаг 2. Интеграция в home рут
Откроем ```routes.py```
```
@app.route("/")
@app.route("/home")
def home():
    #http://localhost:8000/home?page=2
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=4)
    return render_template("home.html" , posts=posts)
```
Теперь изменим home.html
```
{% for post in posts.items %}
```
Поменяли эту строку лишь потому что ```posts``` теперь не список, а объект ```SQLAclhemy.Paginator```. И для того, чтобы получить доступ к постам, нужно обратиться к полю ```posts.items```.

### Шаг 3. Интеграция ссылок на другие страницы.
Чтобы узнать доступные страницы:
```
>>> posts = Post.query.paginate(page=1, per_page=2)
>>> for page in posts.iter_pages():
...     print(page)
...
1
2
3
4
5
6
>>>
```

Теперь интегрируем эту идею в шаблон ```home.html```
```
    {% for page_num in posts.iter_pages() %}
        {% if page_num %}
          <a class="btn btn-outline-info md-4" href="{{ url_for('home', page=page_num)}}">{{ page_num }}</a>
        {% else %}
        {% endif %}
    {% endfor %}
```

### Шаг 4. Подсветка текущей страницы
В шаблоне ```home.html``` исправим блок пагинации:
```
{% if posts.page == page_num %}
            <a class="btn btn-info md-4" href="{{ url_for('home', page=page_num)}}">{{ page_num }}</a>
          {% else %}
            <a class="btn btn-outline-info md-4" href="{{ url_for('home', page=page_num)}}">{{ page_num }}</a>
          {% endif %}
```

Если страниц очень много, то объект ```posts.iter_pages()``` можно настроить следующим образом:
```
.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)
```
Теперь ваши страницы будут разделены друг от друга многоточием
```
1 .....12 13
```

### Шаг 5. Отобразим новые посты сверху, а тухлые - в самом конце
В руте ```home``` добавим промежуточный метод, генерирующий ```SQL``` запрос ```ORDER BY```

```
@app.route("/")
@app.route("/home")
def home():
    #http://localhost:8000/home?page=2
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("home.html" , posts=posts)
```


### Шаг 6. Профилирование
Создадим рут, который будет отображать посты данного пользователя
```
@app.route('/user/<username>/info')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.data_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)

```

Теперь нам нужен шаблон ```user_posts.html```
```
{% extends "base.html" %}


{% block title %}{{ user.username }}'s posts{% endblock %}

{% block content %}
    <h1 class="mb-3">
        Posts by {{ user.username }} ({{ posts.total }})
    </h1>
    {% for post in posts.items %}
        <article class="media content-section">
          <img class="rounded-circle article-img" src="{{ url_for('static', filename='media/' + post.author.image_file)}}">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="{{ url_for('user_posts', username=post.author.username )}}">{{ post.author.username }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</small>
            </div>
            <h2><a class="article-title" href="{{ url_for('post_detail', post_id=post.id)}}">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
    {% endfor %}

    {% for page_num in posts.iter_pages() %}
        {% if page_num %}
          {% if posts.page == page_num %}
            <a class="btn btn-info md-4" href="{{ url_for('home', page=page_num)}}">{{ page_num }}</a>
          {% else %}
            <a class="btn btn-outline-info md-4" href="{{ url_for('home', page=page_num)}}">{{ page_num }}</a>
          {% endif %}
        {% else %}
        {% endif %}
    {% endfor %}
{% endblock content %}
```

***Теперь везде, где есть ссылки на пользователя сервиса (конркетно где стоит username) добавим  линку 
```
  href="{{ url_for('user_posts', username=post.author.username )}}"
```

### Шаг 7. Пагинация конкретного юзера
В шаблоне ```user_posts.html``` исправим пагинацию
```
    {% for page_num in posts.iter_pages() %}
        {% if page_num %}
          {% if posts.page == page_num %}
            <a class="btn btn-info md-4" href="{{ url_for('user_posts', page=page_num, username=user.username)}}">{{ page_num }}</a>
          {% else %}
            <a class="btn btn-outline-info md-4" href="{{ url_for('user_posts', page=page_num, username=user.username)}}">{{ page_num }}</a>
          {% endif %}
        {% else %}
        {% endif %}
    {% endfor %}
```

### Шаг 8. Внедрение профиля
Скопируем профиль из шаблона ```account.html``` и добавим в ```user_posts.html```:
```
  .....
    <div class="content-section">
        <div class="media">
            <img class="rounded-circle account-img" src="{{ url_for('static', filename='media/' + user.image_file) }}">
            <div class="media-body">
                <h2 class="account-heading">{{ user.username }}</h2>
                <p class="text-secondary">{{ user.email }}</p>
            </div>
        </div>
    </div>
    ......
```

### Шаг 9. Добавим плашку last seen
Немного обновим нашу модель (добавим поле last_seen)
```
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password_hash = db.Column(db.String(128), nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.now) # Новое поле
    posts = db.relationship('Post', backref='author', lazy=True)
```

Накатим миграции.

### Шаг 10. Как обновлять это поле?
Идея - каждый раз, когда пользователь (аутентифицированный)  запрашивает url, напишем функцию, которая бдует сначала обновлять поле ```last_seen``` , а потом перенаправлять на нужную страницу.
Как этого добиться?
В ```flask``` существует такой декоратор, который называется ```@app.before_request```. Заходим в ```routes.py```
```
from datetime import datetime

# Выполняется перед каждым запросом!
# Для этого декоратора не важно - залогинен ли юзер или нет.
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

```

Теперь отобразим в шаблоне, когда юзер был последний раз:
```user_posts.html```
```
....    
        <h2 class="account-heading">{{ user.username }}</h2>
                <p class="text-secondary">{{ user.email }}</p>
                {% if user.last_seen %}
                    <p class="text-secondary text-muted">
                        Last seen on: {{ user.last_seen.strftime('%Y-%m-%d %H:%M')}}
                    </p>
                {% endif %}
.....
```
