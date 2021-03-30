# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:22:39
# @Author  : autohe 
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 配置文件
# @Version : $Id$



import os
import sys
# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

#数据库链接地址
basedir = os.path.abspath(os.path.dirname(__file__))
dev_db = prefix + os.path.join(basedir, 'data.db')


class Config:
    """配置信息"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
    #本地加载bootstrap
    BOOTSTRAP_SERVE_LOCAL = True

class DevelopmentConfig(Config):
    """开发环境配置"""
    MYBLOG_POST_PER_PAGE = 5
    MYBLOG_COMMENT_PER_PAGE = 15
    MYBLOG_MANAGE_POST_PER_PAGE = 15
    #BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    DEBUG = True

class ProductConfig(Config):
    '''生产环境配置'''

config_map = {
    "develop" : DevelopmentConfig,
    "product" : ProductConfig
}

