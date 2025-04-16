from flask import Blueprint
from app.controllers import fornecedor_controller

fornecedor_bp = Blueprint('fornecedores', __name__, url_prefix='/fornecedores')

@fornecedor_bp.route('/lista', methods=['GET'])
def lista_fornecedores():
    return fornecedor_controller.listar_fornecedores()

@fornecedor_bp.route('/contato', methods=['POST'])
def contato_fornecedor():
    return fornecedor_controller.solicitar_contato()
