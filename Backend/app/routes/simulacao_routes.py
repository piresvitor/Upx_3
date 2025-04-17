from flask import Blueprint
from app.controllers import simulacao_controller

simulador_bp = Blueprint('simulador', __name__, url_prefix='/simulador')

simulador_bp.route('/enviar', methods=['POST'])
def enviar_dados():
    return simulacao_controller.enviar_dados_consumo()

simulador_bp.route('/resultado/<int:simulacao_id>', methods=['GET'])
def obter_resultado(simulacao_id):
    return simulacao_controller.obter_resultado_simulacao(simulacao_id)
