from flask import request, jsonify
from app.models.user_model import User, db
from flask_jwt_extended import create_access_token

def cadastro():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if User.query.filter_by(email=email).first():
        return jsonify({"erro": "Usuário já cadastrado."}), 400

    novo_usuario = User(email=email)
    novo_usuario.set_password(senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário cadastrado com sucesso."}), 201

def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    usuario = User.query.filter_by(email=email).first()
    if usuario and usuario.check_password(senha):
        token = create_access_token(identity=usuario.email)  # ou 'usuario.id' se preferir
        return jsonify({"token": token}), 200

    return jsonify({"erro": "Credenciais inválidas."}), 401

def logout():
    # Como JWT é stateless, logout geralmente é feito no frontend (removendo o token)
    return jsonify({"mensagem": "Logout efetuado com sucesso (token descartado no frontend)."}), 200
