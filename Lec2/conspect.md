# Лекция 2.
## Шаблоны и встроенный шаблонизатор.

***Задача*** - добавить к нашему проекту возможность выводить информаию с использованием ```HTML``` -шаблонов.

### Шаг 1. Не надо так делать
Все , что мы будем описывать в данной лекции по своей сути работает следующим образом.
```app/routes.py```
```
from app import app 

@app.route("/home")
@app.route("/")
def homepage():
    current_user = {'username' : 'Evgeny Vlasov'}
    return """
    <html>
        <head>
            <title>HomePage</title>
        </head>
        <body>
            <h1>Hello from HomePage!<h1>
            <p>Your username is """ + current_user["username"] + """! </p>
        </body>
    </html>
    """

```

В данном случае функция ```homepage()``` возвращает набор символов, которые могут быть протранслированы браузером и восприняты им как ```html``` код. А что если мы вместо возврата строки будем возвращать настоящий ```html``` файл?

### Шаг 2. Как надо делать
* Создадим директорию ```app/templates```
* Определим файл ```app/templates/home.html```
```
<!-- Это комментарий -->
<!-- app/templates/home.html -->
<!DOCTYPE html>
<html>
    <head>
        <title>HomePage</title>
    </head>
    <body>
        <h1>Hello Homepage</h1>
        <p>Your name is Evgeny Vlasov!</p>
    </body>
</html>
```

* Изменим ```app/routes.py```
```
from app import app 
from flask import render_template

@app.route("/home")
@app.route("/")
def homepage():
    #current_user = {'username' : 'Evgeny Vlasov'}
    return render_template('home.html')
```


### Шаг 3. Шаблонизатор Jinja2
Может возникнуть вопрос - а как передать какую-либо информацию из моего приложения в ```html``` шаблон?
***Jinja2*** - это транслятор (адаптер), который позволяет передавать объекты из языка программирования (в нашем случае Python) в html шаблоны.
#### Передача простейшего аргумента 
И базовый синтаксис шаблонизатора Jinja2.
Для того, чтобы передать объект в ```html``` шаблон, нужно:
* определить объект типа ```key:value``` внутри функции ```routes```
* передать данный объект как аргумент ```context``` в функцию:
```
from flask import render_template

@app.route("/")
def home():
    user = {"username" : "Bob"}
    return rendet_template('path_to_html.html', context=user)
```
* После этого внутри ```path_to_html.html``` считаем данные из ```context```
```
    <h1> Hello {{ context.username }}
```
Происходит обращение типа ```context["username"]``` (это как было бы на Python)

### Шаг 4. Синтаксис шаблонизатора
* ```{{ ... }}``` обозначают вставку значения в определенное место шаблона (ИМЕННО ВСТАВКА ЗНАЧЕНИЯ, А НЕ ВЫПОЛНЕНИЯ ФУНКЦИИ ИЛИ ВЫРАЖЕНИЯ)
* Условный оператор обозначается как :
```
{% if expression %}
    ....
{% endif %}
```
С оператором else:
```
{% if expression %}
    ....
{% else %}
    ....
{% endif %}
```

* Цикл (есть только for) обозначается так:
```
{% for item in items %}
    ...
{% endfor %}
```
где ```items``` - итерируемый объект. Для обозначения момента, когда ***НИ ОДНОЙ*** итерации не было выполнено:
```
{% for item in items %}
    ....
{% empty %}
    ...
{% endfor %}
```


Пример того, что у нас получилось в итоге:
```
<!-- Это комментарий -->
<!-- app/templates/home.html -->
<!DOCTYPE html>
<html>
    <head>
        <title>HomePage</title>
    </head>
    <body>
        <h1>Hello Homepage</h1>
        <p>Your name is {{ context.current_user.username }}. </p>
        {% if context.current_user.age > 18 %}
            <p>Your age is {{ context.current_user.age }}.</p>
            <p>You can pay by credit card.</p>
        {% else %}
            <p>You can not pay by your credit card!</p>
        {% endif %}
        <hr>

        <h3>List of all posts by {{ context.current_user.username }}</h3>
        {% for post in context.posts %}
            <p>{{ post }}</p>
        {% endfor %}
    </body>
</html>
```


### Шаг 5. Наследование шаблонов
Создадим файл ```app/templates/base.html```
```
<!DOCTYPE html>
<html>
    <head>
        <title>
            {% block title %}{% endblock %}
        </title>
        <body>
            {% block content %}
            {% endblock %}
        </body>
    </head>
</html>
```

Встроим ```home.html```
```
{% extends 'base.html' %}

{% block title %}Hello Homepage{% endblock %}

{% block content %}
        <h1>Hello from this Homepage!</h1>
        <p>Your name is {{ context.current_user.username }}. </p>
        {% if context.current_user.age > 18 %}
            <p>Your age is {{ context.current_user.age }}.</p>
            <p>You can pay by credit card.</p>
        {% else %}
            <p>You can not pay by your credit card!</p>
        {% endif %}
        <hr>

        <h3>List of all posts by {{ context.current_user.username }}</h3>
        {% for post in context.posts %}
            <p>{{ post }}</p>
        {% endfor %}
{% endblock %}
```
