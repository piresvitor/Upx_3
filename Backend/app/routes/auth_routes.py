from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user_model import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(senha):
        return jsonify({'erro': 'Credenciais inválidas.'}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify({'token': access_token}), 200

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not nome or not email or not senha:
        return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'erro': 'Usuário já cadastrado.'}), 400

    novo_usuario = User(nome=nome, email=email)
    novo_usuario.set_password(senha)

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário cadastrado com sucesso.'}), 201

@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Como o JWT é stateless, não há "sessão" para invalidar no backend,
    # logout é apenas descartar o token no client side.
    return jsonify({"mensagem": "Logout efetuado com sucesso (token descartado no frontend)."}), 200
