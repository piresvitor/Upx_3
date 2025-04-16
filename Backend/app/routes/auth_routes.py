from flask import Blueprint, request, jsonify
from app.controllers import auth_controller

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    return auth_controller.login()

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    return auth_controller.cadastro()

@auth_bp.route('/logout', methods=['GET'])
def logout():
    return auth_controller.logout()
