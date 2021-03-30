# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:22:39
# @Author  : autohe 
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 登录鉴权
# @Version : $Id$
    
from flask import Blueprint



auth_bp = Blueprint('auth', __name__)

from app.views.auth import views
