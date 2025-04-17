from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Inicializa a instância db

def create_app():
    app = Flask(__name__)
    
    # Configurações principais
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Opcional, para evitar warnings
    app.config['SECRET_KEY'] = 'sua_chave_secreta'

    # Inicializa banco de dados com a aplicação
    db.init_app(app)

    # Registra os blueprints (rotas organizadas)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.simulacao_routes import simulador_bp
    app.register_blueprint(simulador_bp)
    from app.routes.fornecedor_routes import fornecedor_bp
    app.register_blueprint(fornecedor_bp)
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    return app

from app.models import user_model, simulacao_model, fornecedor_model