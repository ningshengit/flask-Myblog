# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:50:35
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$

from flask import (render_template, request, current_app, request, url_for,
                flash, redirect)
from flask_login import current_user
from app.extensions import db
# from bluelog.app.blog import blog_bp
from app.models import Post, Tags, Comment
from app.forms import CommentForm
from app.views.main import blog_bp


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)

@blog_bp.route('/post/<int:post_id>', methods=['POST', 'GET'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items

    form = CommentForm()
    if current_user.is_authenticated:
        from_admin = True
        reviewed = True
    else:
        from_admin = False
        reviewed = False  

    if form.validate_on_submit():
        author = form.author.data
        body = form.body.data
        comment = Comment(author=author, body=body, post_id=post.id, from_admin=from_admin,
                         reviewed=reviewed)
        #如果rul中有reply则认为是对评论的回复
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论已经成功', 'success')
        else:
            flash('感谢大佬指点，很快将会显示评论', 'info')
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, comments=comments, pagination=pagination, form=form)

@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('无法评论.', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


@blog_bp.route('/tag/<int:tag_id>')
def show_tag(tag_id):
    tag = Tags.query.get_or_404(tag_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(tag).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/tag.html', tag=tag, posts=posts, pagination=pagination)


