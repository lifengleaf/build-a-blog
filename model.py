from app import db
from datetime import datetime
from hashutil import make_hash

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pubdate = db.Column(db.DateTime)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, pubdate, owner):
        self.title = title
        self.body = body
        if pubdate is None:
            pubdate = datetime.utcnow()
        self.pubdate = pubdate
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref="user")

    def __init__(self, username, password):
        self.username = username
        self.password = make_hash(password)