from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Inicialize a instância db aqui

def create_app():
    app = Flask(__name__)
    
    # Configurações principais
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Opcional, para evitar warnings

    # Inicializa banco de dados com a aplicação
    db.init_app(app)

    # Registra os blueprints (rotas organizadas)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.fornecedor_routes import fornecedor_bp
    app.register_blueprint(fornecedor_bp)

    return app

from app.models import user_model
from app.models import fornecedor_model