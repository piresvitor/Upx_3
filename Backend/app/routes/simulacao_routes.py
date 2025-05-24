from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import simulacao_controller

simulador_bp = Blueprint('simulador', __name__, url_prefix='/simulador')

@simulador_bp.route('/enviar', methods=['POST'])
@jwt_required()
def enviar_dados():
    user_email = get_jwt_identity()
    return simulacao_controller.enviar_dados_consumo(user_email)

@simulador_bp.route('/resultado/<int:simulacao_id>', methods=['GET'])
@jwt_required()
def obter_resultado(simulacao_id):
    user_email = get_jwt_identity()
    return simulacao_controller.obter_resultado_simulacao(simulacao_id, user_email)

@simulador_bp.route('/lista', methods=['GET'])
@jwt_required()
def listar_simulacoes():
    user_email = get_jwt_identity()
    return simulacao_controller.listar_simulacoes_usuario(user_email)