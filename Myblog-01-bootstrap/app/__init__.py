# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:22:39
# @Author  : autohe 
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 创建空flask web项目脚本
# @Version : $Id$

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
# import click

from flask import Flask
from config import config_map
# from flask_login import current_user
from app.extensions import bootstrap#, db, 
#         csrf, moment, migrate, login_manager, ckeditor)#ckeditor mail, toolbar, login_manager, 

# from bluelog.app.errors import errors_bp
# from bluelog.app.auth import auth_bp
# from bluelog.app.admin import admin_bp
# from bluelog.config import config_map
# from bluelog.models import Admin, Post, Category, Comment

# from flask_wtf.csrf import CSRFError 


def create_app(config_name=None):
    if config_name is None:   
        config_name = os.getenv('FLASK_CONFIG', 'develop')
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    #配置日志
    #记录日志到文件中,设置日志级别等
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/Myblog.log', maxBytes=10240,
                                       backupCount=10)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Myblog startup')


    #注册扩展
    register_extensions(app)
    # #注册蓝图
    register_blueprints(app)
    # #注册命令
    # register_commands(app)
    # #注册上下文处理器
    # register_template_context(app)
    # #错误处理
    # register_errors(app)

    return app

def register_extensions(app):

    bootstrap.init_app(app)
    # db.init_app(app)
    # login_manager.init_app(app)
    # csrf.init_app(app)
    # ckeditor.init_app(app)
    # #mail.init_app(app)
    # moment.init_app(app)
    # #toolbar.init_app(app)
    # migrate.init_app(app, db)

def register_blueprints(app):
    from app.views.main import blog_bp
    app.register_blueprint(blog_bp)
    # app.register_blueprint(errors_bp)
    # app.register_blueprint(auth_bp)
    # app.register_blueprint(admin_bp)