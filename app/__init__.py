from flask import Flask  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from os import path
from .CREDS import SECRET_KEY




db = SQLAlchemy()

DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True

    db.init_app(app)


    from .views import views

    app.register_blueprint(views, url_prefix="/")


    from .models import User

    return app, db