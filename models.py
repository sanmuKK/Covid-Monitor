from flask_login import UserMixin
from config import db
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.String(64),primary_key=True)
    name=db.Column(db.String(16))
    password=db.Column(db.String(32))
    avatar=db.Column(db.String(64))
    comment = db.relationship('Comment', backref='owner_user', cascade='all, delete-orphan', passive_deletes=True)
    reply = db.relationship('Reply', backref='owner_user_reply', cascade='all, delete-orphan', passive_deletes=True)
    def __repr__(self):
        return '<User %r>'%self.id

class Comment(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer,primary_key=True,autoincrement = True)
    reply = db.relationship('Reply', backref='owner_comment',cascade='all, delete-orphan',passive_deletes = True)
    comments_id = db.Column(db.String(32), db.ForeignKey('users.id', ondelete='CASCADE'))
    comment=db.Column(db.String(450))
    time = db.Column(db.DateTime,default=datetime.now)
    def __repr__(self):
        return '<Comment %r>'%self.id

class Reply(db.Model):
    __tablename__='replies'
    id=db.Column(db.Integer,primary_key=True,autoincrement = True)
    comment=db.Column(db.String(248))
    replies_id = db.Column(db.Integer, db.ForeignKey('comment.id',ondelete = 'CASCADE'))
    replies_id_user = db.Column(db.String(64), db.ForeignKey('users.id', ondelete='CASCADE'))
    time = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return '<Reply %r>'%self.id