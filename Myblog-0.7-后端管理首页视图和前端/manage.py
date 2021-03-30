# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:22:39
# @Author  : autohe 
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 启动文件
# @Version : $Id$


from app import create_app

app = create_app("develop")

if __name__ == '__main__':
    app.run()