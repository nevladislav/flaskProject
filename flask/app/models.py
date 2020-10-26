from app import db
from datetime import datetime
import re
from sqlalchemy.sql import func
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash,  check_password_hash

def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)

post_tags = db.Table('post_tags',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id поста
    title = db.Column(db.String(140)) # заголовок поста
    slug = db.Column(db.String(140), unique=True) # url
    body = db.Column(db.Text) # текст поста
    created = db.Column(db.DateTime, default=func.now()) # дата создания поста

    def __init__(self, *args, **kwargs):
        #вызываем конструктор предка (model)
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)

    def __init__(self, *args, **kwargs):
        #вызываем конструктор предка (model)
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '{}'.format(self.name)

roles_users = db.Table('roles_users',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    
    def set_password(self, password):
	    self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
	    return check_password_hash(self.password_hash, password)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))



    