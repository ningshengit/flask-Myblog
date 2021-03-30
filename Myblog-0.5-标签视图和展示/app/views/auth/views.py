# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 17:08:23
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 
# @Version : $Id$

from flask import render_template, flash, redirect, url_for

from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.views.auth import auth_bp
from app.models import Admin
from app.forms import LoginForm

@auth_bp.route('/login', methods=['POST', 'GET'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('登录成功', 'info')
                #return redirect_back()
                return redirect(url_for('blog.index'))
            flash('密码或者用户名错误', 'warning')
        else:
            flash('没有账户名.', 'warning')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('blog.index'))