from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    tasks=db.relationship('Task',backref='user',lazy=True)

class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(150),nullable=False)
    descp=db.Column(db.Text,nullable=False)
    completed=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    due_date=db.Column(db.DateTime, nullable=True)
    priority=db.Column(db.String(20),nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    