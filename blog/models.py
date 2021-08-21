from datetime import datetime
from .app import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    draft = db.Column(db.Boolean, default=True, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def getJson(self):
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }
        return data