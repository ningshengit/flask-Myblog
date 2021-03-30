# -*- coding: utf-8 -*-
# @Date    : 2021-03-18 22:04:24
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$

from flask import (render_template, request, current_app, request, url_for,
                flash, redirect)
from flask_login import current_user, login_required
from app.extensions import db
from app.models import Post
from app.views.admin import admin_bp


@admin_bp.route('/all/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['MYBLOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page, pagination=pagination, posts=posts)
