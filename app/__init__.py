from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    application = Flask(__name__)

    application.config['SECRET_KEY'] = 'sertao-secret-key'
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

    db.init_app(application)
    login_manager.init_app(application)

    from app import models

    with application.app_context():
        db.create_all()

    from app.routes.auth import auth
    application.register_blueprint(auth)

    from app.routes.loja import loja
    application.register_blueprint(loja)

    from app.routes.admin import admin
    application.register_blueprint(admin)

    return application