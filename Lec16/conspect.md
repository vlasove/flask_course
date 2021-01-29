# Лекция 16. Добавление новых сущностей


***Задача***: убедиться, в чем польза blueprint'ов на примере добавления нвого функционала ***отображения пользовательских шаблонов ошибок***.

### Шаг 1. Создадим пакет ```errors```
Создадим директорию ```app/errors```
Создадим ```app/errors/__init__.py```
Создадим ```app/errors/handlers.py```

### Шаг 2. Наполним файл ```handlers.py```
```
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404_handler(error):
    """
    Это обработчик для Not Found/Bad Request
    """
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403_handler(error):
    """
    Unauth
    """
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500_handler(error):
    """
    Это обработчик для Not Found/Bad Request
    """
    return render_template('errors/500.html'), 500

```

### Шаг 3. Регистрация blueprint errors
В файле ```app/__init__.py```
```
```