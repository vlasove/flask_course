# Лекция 1.
## Базовая конфигурация Flask-проекта

***Задача*** : создать простейший проект, который будет выводить веб-страницу с ***Hello Web!***.

### Шаг 1. Виртуальное окружение
***Виртуальное окружение*** - это заизолированная часть ОС (коробка), внутри которой существуют свои версии пакетов/модулей/библиотек и т.д. Все что находится внутри виртуального окружения никак не влияет на внешние процесс ОС, никак не конфликтует с версиями библиотек в ОС и т.д.

***Очень хорошим инструментов*** для работы с виртуальными окружениями в Python является утилита ```pipenv```.
Для установки ```pip install pipenv```

* Для начала инициализируем окружение: ```pipenv shell```
* Чтобы закрыть окружение ```exit```
* Для повторного открытия окружения ```pipenv shelll``` (подцепит уже существующий Pipfile)
* Для того, чтобы установить что-нибудь в наше окружение используем команду ```pipenv install <packge_name>```
* Для установки ```flask``` : ```pipenv install flask```
* Если вам передали проект, вам достаточно найти ```Pipfile``` и ```Pipfile.lock``` , открыть консоль ```pipenv shell``` и выполнить ```pipenv install``` тем самым , вы загрузите все зависимости сторонненго проекта на ваше компутер.

### Шаг 2. Первое (не очень) приложение на Flask
Создадим файл ```main.py``` и напишем в нем следующую логику:
```
from flask import Flask 

app = Flask(__name__)

@app.route("/")
def homepage():
    return "Hello Web!"

if __name__ == "__main__":
    app.run(debug=True, port="8000")
```

* Запуск сервера осуществляется через ```python main.py```
* Остановка через ```Ctrl+C``` (важно не использовать ```Ctrl+Z```)


### Шаг 3. Классическая декомпозиция Flask-приложений
* Создадим директорию ```app```  - это место где будет жить наше приложение
* Внутри директориии ```app``` определим файл ```__init__.py``` (это нужно для того, чтобы данная директория воспринималась как ***ПАКЕТ***)
```
from flask import Flask 

app = Flask(__name__)

from app import routes
```
* Создадим модуль ```app/routes.py```
```
from app import app

@app.route('/')
def homepage():
    return "Hello Web!"
```

* Теперь изменим ```main.py```. Данный модуль будет служить основной точкой входа в наш проект.
```
from app import app 

if __name__ == "__main__":
    app.run(debug=True, port="8000")
```

* Запускаем из консоли точно также ```python main.py```

### Шаг 4. Как сделать
Хочу сделать так, чтобы при перехода по ссылке "/" и "/home" показывалась одна и та же страница? 
***Ответ*** - можно стакать декораторы:
```
@app.route("/home")
@app.route('/')
def homepage():
    return "Hello Web from Decompose Solution!!"
```

### Шаг 5. Полезно
Иногда бывает полезно иницилазировать приложение flask как приложение-окружения.
* Если вы - боярин (Windows) то можно в консоли прописать ```set FLASK_APP=main.py```
* Если вы - не боярин (MacOS\Linux) (```export FLASK_APP=main.py```)
После этого запуск приложения становится возможным через команду ```flask run``` (по умолчанию запускает порт ```5000```)

Для того,чтобы установить переменную окружения для порта можно использовать 
```
set FLASK_RUN_PORT=8000
```

Для установки переменных окружения можно создать файл ```.env``` (в корне, рядом с ```main.py```):
```
FLASK_APP=main.py
FLASK_RUN_PORT=8000
```
После этого перезапустим окружение (```exite``` -> ```pipenv shell```) при запуске все переменные окружения будут подтянуты из ```.env``` файла.

***Настоятельно рекомендую*** - ```.env``` файл всегда добавлять в ```.gitignore```