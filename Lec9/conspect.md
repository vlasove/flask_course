## Лекция 9

***Задача*** добавить пользовательскую аватарку и создать профиль.

### Шаг 1. Добавление нового route
В ```routes.py``` добавим следующую функцию:
```
@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename='media/' + current_user.image_file)
    return render_template("account.html", image_file=image_file)
```

```image_file``` - это строка, которая содержит в себе путь до аватарки текущего пользователя. Мы можем быт ьуверены, что данный запрос выполнит именно известный нам пользователь, т.к. он закрыт ```@login_required``` декоратором.
После того , как строка ```image_file``` будет считана (напомним, что у Models.User имеется теперь поле image_file, которое по умолчанию совпадает с ```default.png```), мы передаем ее в шаблон ```account.html```.

***Замечание*** поле модели с ассоциировано с названием ```default.png```, это означает, что у нас должна иметься в наличии (в директории ```static```) картинка, с названием ```default.png```. На этапе передачи этой картинки в шаблон мы прописываем ее полный путь как ```static/<folders_name>/ + current_user.image_file```.


В шаблоне ```account.html``` мы отрисовываем данную картинку при помощи блока <img>
```
        <div class="media">
            <img class="rounded-circle account-img" src="{{ image_file }}">
            <div class="media-body">
                <h2 class="account-heading">{{ current_user.username }}</h2>
                <p class="text-secondary">{{ current_user.email }}</p>
            </div>
        </div>
```

###  Шаг 2. Добавим новую кнопку на панель
Зайдем в ```base.html``` и добавим для залогиненного пользователя кнопку ```Account```:
```
......
            <!-- Navbar Right Side -->
            <div class="navbar-nav">
              {% if current_user.is_authenticated %}
                <a class="nav-item nav-link" href="{{ url_for('account') }}">Account</a>
                <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>
              {% else %}
                <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
                <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
              {% endif %}
            </div>  
......
```

### Шаг 3. Форма редактирования пользовательской информации
Хотим на страницу ```/account``` добавить форму редактирования информации , в которой так же будет находиться
блок для загрузки нового изображения.

* Заходим в ```forms.py```
```

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
```

Основное внимание к валидаторам.
Если пользователь (current_user) обновляя информацию запишет в поля формы такие логин и почту, что у кого-то из других пользователей они будут совпадать, то естественно форма должна выбросить исключение.

Но если пользователь (current_user) никакой информации о себе не менял (или поменял только часть полей), то, естественно, в бд уже есть пользователь с такими данными . В этом случае форма тоже будет завершаться с исключением. Для того, чтобы избежать этой проблемы используем механизм:
```
    if username.data != current_user.username:
    ....
```
Который буквально означает следующее: если в поле username формы написано то же самое, что и у ```current_user.username``` (это озанчает, что пользвоатель не менял значение формы), то валидатор запускаться не будет. В противном случае будет выполнена базовая проверка.


* Заходим в ```routes.py``` и определим:
```
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Your account info successfully updated!', 'success')
        return redirect(url_for('account'))

    image_file = url_for('static', filename='media/' + current_user.image_file) #static/media/default.png
    return render_template("account.html", image_file=image_file, form=form)
```

Логика данного запроса нам уже знакома:
* Если это запрос ```GET``` - просто показываем форму
* Если это запрос ```POST``` и форма валидна то: подставляем текущему пользователю данные из формы и сохраняем его в бд.
Обратим внимание на то, что блок ```db.session.add(....)``` отсутствует. Дело в том, что мы используем в окружении ```FLASK_ENV=development``` , данная директива позволяет ```flask_login.UserMixin``` держать указать на пользователя все время своего существования (это значит что пользователь всегда находится в db.session).


### Шаг 4. Добавление картинки.
Начнем с шаблона:
```
<form method="POST" action="" enctype="multipart/form-data">
```
* Блок ```enctype``` говорит о том, что форма будет отправлять не только строковые данные, но еще и какие-то файлы.
```
                <div class="form-group">
                    {{ form.picture.label() }}
                    {{ form.picture(class="form-control-file")}}
                    {% if form.picture.errors %}
                        {% for error in form.picture.errors %}
                            <span class="text-danger">{{ error }}</span></br>
                        {% endfor %}
                    {% endif %}

                </div>
```
Данный блок отрисовывает поле формы, (лейбл, саму кнопку для добавления файла), а также ошибки формы, в случае их наличия.

* Теперь добавим поле в форму ```UpdateAccountForm```
```
from flask_wtf.file import FileField, FileAllowed

class UpdateAccountForm(FlaskForm):
    ....
    picture = FileField(label='Account avatar', validators=[FileAllowed(['jpg', 'png'])])
    ....
```
Поле ```FileField``` позволяет прикреплять файлы , а валиадтор ```FileAllowed```  нужен для того, чтобы отсекать невалидные файловые расширения (смотрит только на расширение файла, а не на его контент).

* Теперь обновим ```routes.py```
```
import secrets
import os

def save_picture(form_picture):
    # Есть одна большая проблема.
    # Многие медиа-файлы имеют одинаковое название
    # Решение данной проблемы заключается в следующем:
    # Генерируем 8-15 случайных символов. Прилепливаем к ним расширение медиа-файла.
    random_hex = secrets.token_hex(8) 
    file_ext = form_picture.filename.split('.')[-1]
    picture_filename = random_hex + "." +  file_ext
    picture_path = os.path.join(app.root_path, 'static/media/' , picture_filename)
    # C:/Users/Desktop/flask2/Lec9/ + static/media/ + iudgy1dg32dg1387dg3.png
    form_picture.save(picture_path)

    return picture_filename



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)
    if request.method == "POST" and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
        flash('Your account info successfully updated!', 'success')
        return redirect(url_for('account'))

    image_file = url_for('static', filename='media/' + current_user.image_file) #static/media/default.png
    return render_template("account.html", image_file=image_file, form=form)

```
Функция ```save_picture``` делает следующие действия:
* Генерирует хеш на 8 символов
* Затем к этой строке приклеивается расширение файла
* После чего прописываем путь до этого файла относительно каталога проекта
* Затем сохраняем файл по выше указанному пути
* Возвращаем имя файла

А внутри функции ```account```
* Валидируем форму
* Если пикчу прилепили, то вызываем ```save_picture```
* Помещаем имя файла в поле ```curent_user.image_file```
* Сохраняем пользователя

