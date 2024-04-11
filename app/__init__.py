from flask import Flask  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from os import path
# from flask_login import LoginManager



db = SQLAlchemy()

DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "alsdjfl;aksjdflla;ksdj;lfkjaeijfajdkj"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True

    db.init_app(app)


    from .views import views
    # from .auth import auth
    # from .admin import admin

    app.register_blueprint(views, url_prefix="/")
    # app.register_blueprint(auth, url_prefix="/")
    # app.register_blueprint(admin, url_prefix="/admin/")


    from .models import User

    # create_database(app)


    # login_manager = LoginManager()

    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app, db