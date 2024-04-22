from project import db
from datetime import datetime
from dataclasses import dataclass
from flask_login import UserMixin


@dataclass(order=True)
class User(UserMixin, db.Model):
    id: int
    name: str
    email: str
    password: str
    date_created: datetime

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    secret_key = db.Column(db.String(200), nullable=False)
    secret_token = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id
