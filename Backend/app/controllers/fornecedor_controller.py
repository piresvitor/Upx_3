from flask import jsonify, request
from app.models.fornecedor_model import db, Fornecedor

def listar_fornecedores():
    estado = request.args.get('estado')
    query = Fornecedor.query
    if estado:
        query = query.filter_by(estado=estado.upper())
    fornecedores = query.all()

    resultado = [
        {
            "id": f.id,
            "nome": f.nome,
            "email": f.email,
            "telefone": f.telefone,
            "cidade": f.cidade,
            "estado": f.estado
        }
        for f in fornecedores
    ]
    return jsonify(resultado), 200

def solicitar_contato():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    mensagem = data.get('mensagem')

    if not nome or not email or not mensagem:
        return jsonify({"erro": "Campos obrigatórios: nome, email, mensagem"}), 400

    # Aqui pode integrar com email, notificações ou apenas salvar (simulação)
    return jsonify({"mensagem": "Contato enviado com sucesso!"}), 200
