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
```