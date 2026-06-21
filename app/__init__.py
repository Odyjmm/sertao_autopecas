from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    application = Flask(__name__)

    application.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    # SECRET_KEY e URI do banco agora vêm de variáveis de ambiente.
    # Em desenvolvimento, se não houver .env, usa um valor padrão (NUNCA usar
    # esse padrão em produção — defina SECRET_KEY no ambiente/arquivo .env).
    application.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'dev-only-key-troque-em-producao'
    )
    application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///banco.db'
    )
    application.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'timeout': 15}
    }
    application.config['SESSION_PERMANENT'] = False

    db.init_app(application)
    login_manager.init_app(application)
    login_manager.login_view = 'auth.login'
    csrf.init_app(application)

    from app import models

    with application.app_context():
        db.create_all()

    from app.routes.auth import auth
    application.register_blueprint(auth)

    from app.routes.loja import loja
    application.register_blueprint(loja)

    from app.routes.admin import admin
    application.register_blueprint(admin)

    from app.routes.carrinho import carrinho
    application.register_blueprint(carrinho)

    from app.routes.pedido import pedido
    application.register_blueprint(pedido)

    from app.routes.devolucao import devolucao
    application.register_blueprint(devolucao)

    @application.template_filter('moeda')
    def moeda_filter(value):
        return f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    return application
