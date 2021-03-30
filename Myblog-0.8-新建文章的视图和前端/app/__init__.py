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
import click

from flask import Flask
from config import config_map
from flask_login import current_user
from app.extensions import bootstrap, db, login_manager, csrf, ckeditor

# from bluelog.app.errors import errors_bp

from app.models import Admin, Tags

# from flask_wtf.csrf import CSRFError 
from flask_migrate import Migrate

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
    register_commands(app)
    # #注册上下文处理器
    register_template_context(app)
    # #错误处理
    # register_errors(app)
    migrate = Migrate(app, db)
    from app import models
    return app

def register_extensions(app):

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    # #mail.init_app(app)
    # moment.init_app(app)
    # #toolbar.init_app(app)
    # migrate.init_app(app, db)

def register_blueprints(app):
    from app.views.main import blog_bp
    app.register_blueprint(blog_bp)
    # app.register_blueprint(errors_bp)
    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app.views.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')


#app_context_processor在flask中被称作上下文处理器，
#借助app_context_processor我们可以让所有自定义变量在模板中可见
#比如返回一个dict类型数据
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        tags = Tags.query.order_by(Tags.name).all()
        #links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            pass#unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, tags=tags)
            #links=links, unread_comments=unread_comments)



def register_commands(app):

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                master='autohe',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()

    @app.cli.command()
    @click.option('--tags', default=10, help='Quantity of tags, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(tags, post, comment):
        """Generate fake data."""
        from app.faker import fake_admin, fake_tags, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % tags)
        fake_tags(tags)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')