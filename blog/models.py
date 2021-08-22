from enum import unique
from flask_login import UserMixin
from datetime import datetime
from .app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, name, password):
        self.name = name
        self.password = password

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    draft = db.Column(db.Boolean, default=True, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def to_dic(self):
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }
        return data