# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:22:39
# @Author  : autohe 
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : 表单文件
# @Version : $Id$


#from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

class LoginForm(FlaskForm):
    name = StringField('管理员', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住')
    submit = SubmitField('登录')

class CommentForm(FlaskForm):
    author = StringField('大佬', validators=[DataRequired(), Length(1, 30)])
    #email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('指点')