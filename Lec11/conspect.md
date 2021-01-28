# Лекция 11. favicon, post CRUD

### Шаг 1. Добавим favicon
Скачаем любую иконку (например https://favicon.io/emoji-favicons/star/)
Вытащим любую пикчу, назовем ее ```favicon.png``` и поместим по пути ```static/favicon/favicon.png```
В базовый шаблон ```base.html``` встроим ссылку:
```
<link rel="icon" href="{{ url_for('static', filename='favicon/favicon.png')}}" type="image/x-icon"/>
```

### Шаг 2. Добавление кнопок в панель навигации
Заходим в ```base.html``` и добавим пару строк:
```
            <div class="navbar-nav">
              {% if current_user.is_authenticated %}
                <a class="nav-item nav-link" href="#">New Post</a>
                <a class="nav-item nav-link" href="{{ url_for('account') }}">{{ current_user.username }}</a>
                <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>

              {% else %}
                <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
                <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
              {% endif %}
            </div>
```

### Шаг 3. Посты
#### Создание поста
```
# forms.py
....
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Create")
```

Подготовим рут:
```
@app.route('/post/create', methods=['GET' , 'POST'])
@login_required
def post_create():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('post_create.html', form=form)
```

Создадим шаблон ```post_create.html```
```
{% extends "base.html" %}

{% block title %}Post Create Page{% endblock %}

{% block content %}
    <div class="content-section">
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Create New Post</legend>
                <div class="form-group">
                    {{ form.title.label(class="form-control-label") }}
                    {% if form.title.errors %}
                        {{ form.title(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.title.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                        {{ form.title(class="form-control form-control-lg") }}
                    {% endif %}
                </div>
                <div class="form-group">
                    {{ form.content.label(class="form-control-label") }}
                    {% if form.content.errors %}
                        {{ form.content(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.content.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                        {{ form.content(class="form-control form-control-lg") }}
                    {% endif %}
                </div>
            </fieldset>
            <div class="form-group">
                {{ form.submit(class="btn btn-outline-info") }}
            </div>
        </form>
    </div>
{% endblock %}
```

#### Отображение всех постов из бд
Обновим рут:
```
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html" , posts=posts)

```

Теперь поправим шаблон отображения списка постов:
```
{% extends "base.html" %}


{% block title %}Home Page{% endblock %}

{% block content %}
    {% for post in posts %}
        <article class="media content-section">
          <img class="rounded-circle article-img" src="{{ url_for('static', filename='media/' + post.author.image_file)}}">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author.username }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</small>
            </div>
            <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
    {% endfor %}
{% endblock content %}
```

#### Детальное отображение поста
Создадим новый рут:
```
@app.route('/post/<int:post_id>/detail')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)
```

Создадим шаблон:
```
{% extends "base.html" %}


{% block title %}{{ post.title }}{% endblock %}

{% block content %}
        <article class="media content-section">
          <img class="rounded-circle article-img" src="{{ url_for('static', filename='media/' + post.author.image_file)}}">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author.username }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</small>
            </div>
            <h2><a class="article-title" href="{{ url_for('post_detail', post_id=post.id)}}">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
{% endblock content %}
```

Данную ссылку добавить во все места, где используются URL для детальных отображений постов:
```
href="{{ url_for('post_detail', post_id=post.id)}}"
```


#### Обновление поста
Создадим рут:
```
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post) # В полях формы уже были данные

    if post.author != current_user:
        abort(403) # Forbidden

    if request.method == 'POST' and form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data 
        db.session.add(post)
        db.session.commit()

        flash('Post has been updated successfully!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post_update.html', post=post, form=form)
```

Теперь под него создадим шаблон ```post_update.html```
```
{% extends "base.html" %}

{% block title %}Post {{ post.title }}{% endblock %}

{% block content %}
    <div class="content-section">
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Update following post</legend>
                <div class="form-group">
                    {{ form.title.label(class="form-control-label") }}
                    {% if form.title.errors %}
                        {{ form.title(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.title.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                        {{ form.title(class="form-control form-control-lg") }}
                    {% endif %}
                </div>
                <div class="form-group">
                    {{ form.content.label(class="form-control-label") }}
                    {% if form.content.errors %}
                        {{ form.content(class="form-control form-control-lg is-invalid") }}
                        <div class="invalid-feedback">
                            {% for error in form.content.errors %}
                                <span>{{ error }}</span>
                            {% endfor %}
                        </div>
                    {% else %}
                        {{ form.content(class="form-control form-control-lg") }}
                    {% endif %}
                </div>
            </fieldset>
            <div class="form-group">
                <button typy="submit" class="btn btn-outline-primary">Update</button>
            </div>
        </form>
    </div>
{% endblock %}
```


Добавим кнопку для обновления поста на шаблон ```post_detail.html```
```
<small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</small>
              {% if post.author == current_user %}
                <a class="btn btn-secondary btn-sm m-2" href="{{ url_for('post_update', post_id=post.id)}}">Update</a>
              {% endif %}
            </div>
```
#### Интересное удаление
Для начала нариусем кнопку удаления:
```
            {% if post.author == current_user %}
                <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{{ url_for('post_update', post_id=post.id)}}">Update</a>
                <button type="button" class="btn btn-danger btn-sm m-1">Delete</button>
              {% endif %}
```
Modal брали отсюда: https://getbootstrap.com/docs/4.0/components/modal/#live-demo

Итоговый ```post_detail.html```
```
{% extends "base.html" %}


{% block title %}{{ post.title }}{% endblock %}

{% block content %}
        <article class="media content-section">
          <img class="rounded-circle article-img" src="{{ url_for('static', filename='media/' + post.author.image_file)}}">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author.username }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d %H:%M') }}</small>
              {% if post.author == current_user %}
                <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{{ url_for('post_update', post_id=post.id)}}">Update</a>
                <button type="button" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#deleteModal">Delete</button>
              {% endif %}
            </div>
            <h2><a class="article-title" href="{{ url_for('post_detail', post_id=post.id)}}">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
        <!-- Modal -->
      <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="deleteModalLabel">Delete Post?</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <p>Are you sure you want to delete this post?</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
              <form action="{{ url_for('post_delete', post_id=post.id )}}" method="POST">
                <input type="submit" class="btn btn-danger" value="Delete">
              </form>
            </div>
          </div>
        </div>
      </div>
{% endblock content %}
```

Теперь создадим рут, который будет удалять:
```
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been successfully deleted!', 'success')
    return redirect(url_for('home'))

```
