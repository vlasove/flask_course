# Лекция 3. Шаблоны (продолжение)

***Задача***: добавить простейшую панель навигации и поддержку ```Bootstrap```.

### Шаг 1. Простейшая панель навигации
Для добавления простейшей панели навигации нужно выполнить одно важное условие:
***панель навигации видна абсолютно на всех страницах***. Для того, чтобы не копировать ```html``` код во всех шаблонах, добавим панель навигации в базовый шаблон. 
В шаблоне ```base.html``` добавим следующий код в ```<body>```
```
    <body>
        <!--Добавление простейшей панели навигации -->
        <div>
            MyAppName : <a href="#">Home</a>
        </div>
        <hr>
        
        {% block content %}
        {% endblock %}
    </body>
```

### Шаг 2. Добавим немного информации про пользовтаеля
Добавим пользователю информацию про электронную почту и его возраст.
Для этого в ```routes.py``` в объект ```user``` включим дополнительные поля:
```
user = {
    'username' : 'Bob',
    'email' : 'bob@mail.ru',
    'age' : 33,
}
```

### Шаг 3. Создадим страницу с информацией про этого пользователя
* Создадим новую функцию:
```
@app.route('/about')
def about():
    return render_template(
        'about.html',
        user=user,
    )
```

* Создадим шаблон ```app/templates/about.html```
```
{% extends 'base.html' %}

{% block title %}About Page{% endblock %}

{% block content %}
    <h1>About page</h1>
    <p>This page contains information about {{ user.username}:}</p>
    <p>
        <b>Name</b> : {{ user.username }}
    </p>
    <p>
        <b>Email</b> : {{ user.email }}
    </p>
    <p>
        <b>Age </b>: {{ user.age }}
    </p>
{% endblock %}
```

### Шаг 4. Добавим ссылки на страницы в панель навигации
* Первый вариант добавления ссылок (не самый удачный вариант) - это захардкодить эти ссылки.
```
 <!--Добавление простейшей панели навигации -->
        <div>
            MyAppName : <a href="/home">Home</a> | <a href="/about">About</a>
        </div>
```

* Второй вариант - используем динамический генератор ```url_for```
```
<!--Добавление простейшей панели навигации -->
        <div>
            MyAppName : <a href="{{ url_for('home') }}">Home</a> 
            |
            <a href="{{ url_for('about') }}">About</a>
        </div>
```

В данном коде под функцией ```url_for('name`)``` - ```name``` - это назыание функции из ```routes.py```


### Шаг 5. Добавление Bootstrap в шаблоны
***Bootstrap*** - это достаточно популярный ```css``` фреймворк, который позволяет использовать достаточно обширную библиотеку стилей и не писать их самим.

Добавить ```Boostrap``` в проект можно двумя способами:
* Скачать исходники и поместить их в папке ```static``` проекта https://getbootstrap.com/docs/5.0/getting-started/download/


* Встроить уже готовые ```cdn``` ссылки в шаблоны 
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">


* В итоге получим ```base.html```:
```
<!DOCTYPE html>
<html>
    <head>
        <title>{% block title %}{% endblock %}</title>
        <!--Поддержка utf-8 из коробки для связки шаблон-клиент -->
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
    </head>
    <body>
        <!--Добавление простейшей панели навигации -->
        <div>
            MyAppName : <a href="{{ url_for('home') }}">Home</a> 
            |
            <a href="{{ url_for('about') }}">About</a>
        </div>
        <hr>

        {% block content %}
        {% endblock %}
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
    </body>
</html>
```
