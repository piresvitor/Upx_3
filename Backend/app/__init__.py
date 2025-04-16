from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models.user_model import db

def create_app():
    app = Flask(__name__)
    # Configurações principais
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    # Inicializa banco de dados
    db.init_app(app)

    # Registra os blueprints (rotas organizadas)
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)

    return app
