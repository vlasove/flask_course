## Лекция №8

### Задача
* Интеграция ```postgresql```
* Интеграция ```static```
* Еще раз повторим ```CRUD```
* Аватарка профиля и простейшая работа с media-файлами
* Если успеем (пагинация)

### Шаг 1. Интеграция postgresql
* Первое - откроем ```pgAdmin```
* Затем создать базу данных с названием ```blogger```

Postgres - это субд. Для подключения к этой субд из нашего проекта нам важно помнить ряд настроек:
* Как зовут пользователя, создавшего бд? ```postgres```
* Пароль данного пользователя? ```#########```
* Хост, где запущена субд? ```127.0.0.1``` / ```localhost```
* Порт, на котором запущена субд? ```5432```
* Название БД, которую создали для проекта? ```blogger```

### Шаг 2. Перенос приложения на postgresql
Для работы Python приложения с сторонней субд необходим ***адаптер***.
Для ```postgresql``` этот адаптер называется ```psycopg2``` : ```pipenv install psycopg2```.

Шаблон ```uri``` для подключения к postgres выглядит следующи образом:
```"postgresql+psycopg2://<username>:<password>@<host>:<port>/<db>"```
* ```<username>``` - Как зовут пользователя, создавшего бд?
* ```<password>```-  Пароль данного пользователя
* ```host``` - Хост, где запущена субд? ```127.0.0.1``` / ```localhost```
* ```port``` - Порт, на котором запущена субд? ```5432```
* ```db``` - Название БД, которую создали для проекта? ```blogger```

В связи с данными параметрами, обновим файл ```config.py```
```
import os 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}".format(
        user=os.environ.get("DB_USER"),
        pw=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        db=os.environ.get("DB_NAME")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Соответственно, в файл ```.env``` необходимо добавить 5 новых переменных
```
DB_USER= "postgres"
DB_NAME="blogger"
DB_PASSWORD="########"
DB_HOST="127.0.0.1"
DB_PORT="5432"
```

### Шаг 3. Миграции в postgresql
После обновления ```config.py``` и ```.env``` выполним стандартные команды:
```
flask db init
flask db migrate -m "init"
flask db upgrade
```
