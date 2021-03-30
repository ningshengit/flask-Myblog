# -*- coding: utf-8 -*-
# @Date    : 2021-03-18 22:04:24
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$
import os 
from flask import (render_template, request, current_app, request, url_for,
                flash, redirect)
from flask_login import current_user, login_required
from app.extensions import db
from app.models import Post,Tags
from app.views.admin import admin_bp
from app.forms import PostForm
from flask_ckeditor import upload_success, upload_fail



@admin_bp.route('/all/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['MYBLOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page, pagination=pagination, posts=posts)

@admin_bp.route('/all/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        tag = Tags.query.get(form.tag.data)
        post = Post(title=title, body=body, tag=tag)
        db.session.add(post)
        db.session.commit()
        flash('文章已经提交', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/all/post/edit/<int:post_id>', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.tag = Tags.query.get(form.tag.data)
        #使用get( )方法， 根据id（ 主键 ）来获取对应行数据
        #上面已经修改post的内容，因此直接commit
        db.session.commit()
        flash('文章已经更新', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.tag.data = post.tag_id
    return render_template('admin/edit_post.html', form=form)

@admin_bp.route('/all/post/set-comment/<int:post_id>', methods=['POST'])
@login_required
def set_comment(post_id):
    post = Post.query.get_or_404(post_id)
    if post.can_comment:
        post.can_comment = False
        flash('设置禁止评论', 'success')
    else:
        post.can_comment = True
        flash('设置可以评论', 'success')
    db.session.commit()
    return redirect(url_for('admin.manage_post'))

@admin_bp.route('/all/post/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已经删除', 'success')
    return redirect(url_for('admin.manage_post'))    

@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
    f = request.files.get('upload')  # 获取上传图片文件对象
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:  # 验证文件类型示例
        return upload_fail(message='Image only!')  # 返回upload_fail调用
    f.save(os.path.join('/upload', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url) # 返回upload_success调用


