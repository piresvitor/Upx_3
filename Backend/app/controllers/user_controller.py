from flask import jsonify, request
from app.models.user_model import User
from app import db
from app.utils.jwt_manager import decode_token

def obter_dados_usuario():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"erro": "Token de autenticação não fornecido."}), 401

    # Remover o prefixo "Bearer " se presente
    if token.startswith('Bearer '):
        token = token[7:]
   
    user_id = decode_token(token)
    if not user_id:
        return jsonify({"erro": "Token de autenticação inválido."}), 401
    print(f"Tipo de user_id: {type(user_id)}, Valor de user_id: {user_id}") 
    user = User.query.get(user_id)

    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    return jsonify({
        "id": user.id,
        "nome": user.nome,
        "email": user.email
    }), 200

def editar_usuario():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"erro": "Token de autenticação não fornecido."}), 401

    # Remover o prefixo "Bearer " se presente
    if token.startswith('Bearer '):
        token = token[7:]

    user_id = decode_token(token)
    if not user_id:
        return jsonify({"erro": "Token de autenticação inválido."}), 401
    print(f"Tipo de user_id: {type(user_id)}, Valor de user_id: {user_id}")

    user = User.query.get(user_id)
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

def deletar_usuario():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"erro": "Token de autenticação não fornecido."}), 401

    # Remover o prefixo "Bearer " se presente
    if token.startswith('Bearer '):
        token = token[7:]

    user_id = decode_token(token)
    if not user_id:
        return jsonify({"erro": "Token de autenticação inválido."}), 401
    print(f"Tipo de user_id: {type(user_id)}, Valor de user_id: {user_id}")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"mensagem": "Usuário deletado com sucesso."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao deletar usuário: {str(e)}"}), 500
