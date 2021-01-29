from flask import Blueprint, abort, redirect, url_for, flash, request, render_template
from .forms import PostForm
from app.models import Post
from app import db 
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been successfully deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post_detail', post_id=post.id))
    return render_template('post_update.html', post=post, form=form)

@posts.route('/post/<int:post_id>/detail')
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)


@posts.route('/post/create', methods=['GET' , 'POST'])
@login_required
def post_create():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('post_create.html', form=form)