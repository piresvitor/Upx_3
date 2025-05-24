from flask import jsonify, request
from app.models.user_model import User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def obter_dados_usuario():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(email=user_identity).first()

    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    return jsonify({
        "id": user.id,
        "nome": user.nome,
        "email": user.email
    }), 200

@jwt_required()
def editar_usuario():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(email=user_identity).first()

    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"erro": "Nenhum dado fornecido para atualização."}), 400

    if 'nome' in data:
        user.nome = data['nome']
    if 'email' in data:
        existing_user = User.query.filter(User.email == data['email'], User.id != user.id).first()
        if existing_user:
            return jsonify({"erro": "Este email já está em uso."}), 400
        user.email = data['email']

    try:
        db.session.commit()
        return jsonify({"mensagem": "Dados do usuário atualizados com sucesso."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar dados do usuário: {str(e)}"}), 500

@jwt_required()
def deletar_usuario():
    user_identity = get_jwt_identity()
    user = User.query.filter_by(email=user_identity).first()

    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"mensagem": "Usuário deletado com sucesso."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao deletar usuário: {str(e)}"}), 500
