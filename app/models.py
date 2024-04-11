from . import db 
# from flask_login import UserMixin
# from sqlalchemy import func
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(200))
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)