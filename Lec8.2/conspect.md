## Лекция 8 (продолжение)

*** Декомпозируем исходный код в соответствии с принятым нами шаблоном***
По итогу должна получиться следующая структура:
```
C:.
│   .env
│   .gitignore
│   config.py
│   conspect.md
│   main.py
│   Pipfile
│   Pipfile.lock
│
├───app
│   │   forms.py
│   │   models.py
│   │   routes.py
│   │   __init__.py
│   │
│   ├───static
│   │   ├───css
│   │   │       base.css
│   │   │
│   │   └───media
│   └───templates
│           about.html
│           base.html
│           home.html
│           login.html
│           register.html
│
└───migrations
    │   alembic.ini
    │   env.py
    │   README
    │   script.py.mako
    │
    └───versions
            d3b16d85afee_init.py
```