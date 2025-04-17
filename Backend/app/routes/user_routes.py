from flask import Blueprint
from app.controllers import user_controller

user_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@user_bp.route('/dados', methods=['GET'])
def obter_dados():
    return user_controller.obter_dados_usuario()

@user_bp.route('/editar', methods=['PUT'])
def editar():
    return user_controller.editar_usuario()

@user_bp.route('/deletar', methods=['DELETE'])
def deletar():
    return user_controller.deletar_usuario()
