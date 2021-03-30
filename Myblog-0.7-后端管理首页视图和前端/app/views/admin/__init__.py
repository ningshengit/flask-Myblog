# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:22:39
# @Author  : autohe 
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 管理后台的初始化
# @Version : $Id$
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

from app.views.admin import views
