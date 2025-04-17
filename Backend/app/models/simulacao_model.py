from app import db
from datetime import datetime

class Simulacao(db.Model):
    __tablename__ = 'simulacoes'

    id = db.Column(db.Integer, primary_key=True)
    consumos_kwh = db.Column(db.JSON, nullable=False) # Lista de consumos mensais
    tarifa_atual = db.Column(db.Float, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    resultado = db.Column(db.JSON) # Armazenará os resultados da simulação

    def __repr__(self):
        return f'<Simulacao {self.id}>'
    