from exts import db
from datetime import datetime


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    priority = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
