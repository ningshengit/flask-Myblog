# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:46:24
# @Author  : autohe (${email})
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : extensions扩展
# @Version : $Id$

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
# from flask_moment import Moment
# from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_ckeditor import CKEditor

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
# moment = Moment()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from app.models import Admin
    user = Admin.query.get(int(user_id))
    return user
    
login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

# login_manager.refresh_view = 'auth.re_authenticate'
# # login_manager.needs_refresh_message = 'Your custom message'
# login_manager.needs_refresh_message_category = 'warning'