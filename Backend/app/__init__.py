from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configurações CORS
    CORS(app)  # Libera todas as origens

    # Configurações principais 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua_chave_secreta'
    app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_para_jwt'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    # Inicializa extensões
    jwt = JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Registra blueprints
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.simulacao_routes import simulador_bp
    app.register_blueprint(simulador_bp)
    from app.routes.fornecedor_routes import fornecedor_bp
    app.register_blueprint(fornecedor_bp)
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    # Swagger
    from app.routes.documentacao import swagger_bp, swaggerui_blueprint
    app.register_blueprint(swagger_bp)
    app.register_blueprint(swaggerui_blueprint)

    return app

from app.models import user_model, fornecedor_model