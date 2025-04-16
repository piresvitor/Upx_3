from app import create_app
from app.models.user_model import db
from app.models import consumo_model, simulacao_model, fornecedor_model

app = create_app()

with app.app_context():
    db.create_all()
    print("Banco de dados com todos os modelos criado com sucesso!")
