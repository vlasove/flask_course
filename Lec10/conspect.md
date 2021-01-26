## Лекция 10

***Задача*** реализовать CRUD для постов.

### Шаг 1. Реализация формы поста

В файле ```forms.py``` добавим форму создания поста.
```
...
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField

...

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')

```

### Шаг 2. Реализация создания поста
* В ```routes.py``` создадим новую функцию
```
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', form=form)
```

* В ```create_post.html```
```
{% extends "base.html" %}

{% block title %}Create New Post{% endblock %}


{% block content %}
<div class="content-section">
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">New Post</legend>
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
{% endblock content %}
```

* В ```base.html``` добавим поле ```New Post```
```
                {% if current_user.is_authenticated %}
                <a class="nav-item nav-link" href="{{ url_for('new_post') }}">New Post</a>
                <a class="nav-item nav-link" href="{{ url_for('account') }}">Account</a>
                <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>
              {% else %}
                <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
                <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
              {% endif %}
``` 

* А в ```home.html``` 
```
{% extends "base.html" %}


{% block title %}Home Page{% endblock %}

{% block content %}
    {% for post in posts %}
        <article class="media content-section">
          <img class="rounded-circle account-img" src="{{ url_for('static', filename='media/' + post.author.image_file)}}">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author.username }}</a>
              <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
            </div>
            <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
    {% endfor %}
{% endblock content %}
```