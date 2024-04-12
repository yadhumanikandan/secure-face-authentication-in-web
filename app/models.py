from . import db 
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(200))
    code = db.Column(db.String(200), nullable=True)
    otp = db.Column(db.String(10), nullable=True)
