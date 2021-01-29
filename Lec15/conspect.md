# Лекция 15. Декомпозиция для Flask-Blueprint

# Шаг 1. Разделение сущностей.
* ```users``` - сущность, отвечающая за работу с пользователем
* ```posts``` - сущность, отвечающая за работу с постами
* ```main``` - все остальное

Создадим 3 директории внутри ```app```:
* ```app/users/```
* ```app/posts/```
* ```app/main/```

### Шаг 2. Пакетирование сущностей
Содать:
* ```app/users/__init__.py```
* ```app/main/__init__.py```
* ```app/posts/__init__.py```

В каждый из этих пакетов добавим по файлу ```routes.py```
* ```app/users/routes.py```
* ```app/posts/routes.py```
* ```app/main/routes.py```

### Шаг 3. Определим, где есть формы?
Создадим в тех приложения, где необходим ввод данных модули ```forms.py```
* ```app/posts/forms.py```
* ```app/users.forms.py```

### Шаг 4. Вспомогательные функции - в ```utils.py```
Поскольку вспомогательные фукнции имеют отношение только в пользователям, создадим:
* ```app/users/utils.py```


### Шаг 5. Интеграция ```Blueprints```
В ```app/main/routes.py```
```
from flask import Blueprint

main = Blueprint('main', __name__)
```

В ```app/posts/routes.py```
```
from flask import Blueprint

posts = Blueprint('posts', __name__)
```

В ```app/users/routes.py```
```
from flask import Blueprint

users = Blueprint('users', __name__)
```

### Шаг 6. Разбросаем ```app/routes.py``` по приложениям

Все что имеет отношение к пользователю - в ``users/routes.py``` (сторонние функции ```users/utils.py```)
Все что имеет отношение к постам - в ```posts/routes.py```
Все остальное - в ```main/routes.py```

### Шаг 7. Разделение форм
Формы для пользователя - в ```users/forms.py```
Формы для постов - в ```posts/forms.py```

### Шаг 8. Фиксим импорты
Во всех созданных файлах добавим необходимые блоки ```from ... import ...```

### Шаг 9. Удаление лишнего.
Теперь можем удалить ```app/forms.py``` и ```app/routes.py```

### Шаг 10. Перепишем ```app/__init__.py```
```
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


login = LoginManager(app)
login.login_view = 'users.login'
login.login_message_category = 'info'

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main 
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

from app import models

```

### Поправим все обращения через ```url_for()```
Поскольку теперь мы используем ```blueprints``` обращения к нашим рутам внутри приложения будут выглядеть как ```<blueprints_name>.<bluprints_route>```. Например, было ```login```, ```home``` -> станет ```users.login``` , ```main.home```. Эти исправления нужно внести во всех местах нашего проекта (в коде. в шаблонах). Но поскольку именованные обращения используются только в функции ```url_for``` - можно просто устроит ьпоиск по этой функции в проекте.

После исправления во всем проекте - проверим, что все работает как прежде