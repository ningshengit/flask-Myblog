# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:22:39
# @Author  : autohe 
# @知乎    : https://www.zhihu.com/people/kuanye
# @微信    : xdxh-1
# @funtion : models
# @Version : $Id$
    
from datetime import datetime
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(UserMixin, db.Model):
    '''用户表'''
    __tablename__ = 'tbl_admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    master = db.Column(db.String(20))
    about = db.Column(db.Text)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)




class Tags(db.Model):
    '''文章分类表'''
    __tablename__ = 'tbl_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Post', back_populates='tag')
    def delete(self):
        default_tags = Tags.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.tag = default_tags
        db.session.delete(self)
        db.session.commit()   

class Post(db.Model):
    '''文章表'''
    __tablename__ = 'tbl_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tbl_tags.id'))
    tag = db.relationship('Tags', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

class Comment(db.Model):
    '''评论'''
    __tablename__ = 'tbl_comment'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('tbl_post.id'))
    post = db.relationship('Post', back_populates='comments')

    replied_id = db.Column(db.Integer, db.ForeignKey('tbl_comment.id'))
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])