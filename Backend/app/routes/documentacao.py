from flask import Blueprint, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import os

swagger_bp = Blueprint('swagger_file', __name__, url_prefix='/swagger')

# Caminho absoluto para o arquivo swagger.yaml na raiz do projeto
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
SWAGGER_FILE_PATH = os.path.join(ROOT_DIR, 'swagger.yaml')

@swagger_bp.route('/swagger.yaml')
def openapi_yaml():
    """Retorna o arquivo swagger.yaml."""
    return send_from_directory(ROOT_DIR, 'swagger.yaml')

swaggerui_blueprint = get_swaggerui_blueprint(
    '/swagger',                    # URL onde a UI estará disponível
    '/swagger/swagger.yaml',       # Caminho que o Swagger UI usará para buscar o YAML
    config={'app_name': "API de Simulação de Energia Solar"}
)