# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:50:35
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$

from flask import render_template, request, current_app, request, url_for
                #flash, redirect)
#from flask_login import current_user
# from bluelog.extensions import db
# from bluelog.app.blog import blog_bp
from app.models import Post
# from bluelog.forms import AdminCommentForm, CommentForm
from app.views.main import blog_bp


@blog_bp.route('/')
def index():
    # page = request.args.get('page', 1, type=int)
    # per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    # posts = pagination.items
    # print(len(posts))
    return render_template('blog/index.html')
