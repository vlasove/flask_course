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