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
