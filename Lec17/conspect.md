## Лекция 17. Локализация

Вот у нас есть сервис, но он на английском :(
***Хочется*** чтобы если пользователь открывает страницу в СНГ - отображалось на русском (или была возможность выбрать русский язык), или если не СНГ - то на английском.

### Шаг 1. Установка расширения
Расширение ```flask-babel```
Установка ```pipenv install flask-babel```

### Шаг 2. Инициализация сущности
Заходим ```app/__init__.py```
```
.....
from flask_babel import Babel

app = Flask(__name__)
....
babel = Babel(app)
...
```

### Шаг 3. Настройка поддерживаемых языков
Настройка поддерживаемых языков определяется в конфигуративе приложения. Это означает, что нужно открыть файл ```config.py``` и добавить следующую строчку
```
...
class Config:
    ....
    LANGUAGES = ['en', 'ru'] # Но в этом списке можно указать стандартные 2-ух буквенные абреввиатуары всех # языковых семейств
```

### Шаг 4. А в какой момент будет выбираться тот или иной язык?
Для того, чтобы научить приложение выбирать наиболее подходящий язык в данной ситуации, добавим в ```app/__init__.py``` следующую функцию.
```
from flask import request

......
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
```

Каждый запрос имеет следующую плашку:
```
    Accept-Languages: ru, en-us;q=0.5
```
Данную строку можно интерпретировать как свидетельство того, что ```ru``` языковое семейство (имеет вероятность ```1```) более предпочтительно чем языковое семейство ````en-us``` которое имеет вероятность ```0.5```

### Как заставить этот babel переводить информацию
```
flash("HOW-HOW-HOW")
```
Допустим у нас была такая флешка, мы хотим заставить ее отображаться на русском в соответсвующей зоне.

```
from flask_babel import _

flash(_("HOW-HOW-HOW"))
```
Это означает, что строка "HOW-HOW-HOW" теперь будет участвовать в рекомпиляции для языковой зоны.

Для текстовой информации, которая появляется редко, ее можно переводить только в момент отображения:
```
from flask_babel import lazy_gettext as _lg

class LoginForm(FlaskForm):
    email = StringField(_lg("E-mail address", validators=[....]))

```

### После того, как в проекте появлись пометки
Языковые пометки указываются через ```_("....")```или ```_lg("...")```, нужно скомпилировать блок перевода.
Для этого:
* Созаддим в корне файл ```babel.cfg```
```
[python: app/**.py]
[jinja2: app/templates/**.html]
extensions=jinja2.autoescape, jinja2.with_
```

### Установка утилиты
Установка: https://www.gnu.org/software/gettext/

### После установка генерируем каталог
Генерация виртуального каталога
```
pybabel extract -F babel.cfg -k _lg -o messages.pot .
```
Генерация локального каталога русского перевода
```
pybabel init -i messages.pot -d app/locale -l ru
```

Если все ок и ```gettext``` правильно установлен то появится каталог
```
app/locale/ru/LC_MESSAGES/messages.po
```

С начинкой в стиле
```
msgid "HOW-HOW-HOW"
msgstr " ХА-ХА-ХА"

msgid "Email Adddress"
msgstr "E-mail адрес"
...
```
После того, как весь перевод будет заполнен - выполните компиляцию всего каталога:
```
pybabel compile -d app/locale
```
Только после этого на странице будут изображаться валидные данные в соответствии с вашей языковой зоной.


