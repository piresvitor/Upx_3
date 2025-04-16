from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SimulacaoSolar(db.Model):
    __tablename__ = 'simulacoes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    economia_estimativa = db.Column(db.Float, nullable=False)
    investimento_estimado = db.Column(db.Float, nullable=False)
    retorno_anos = db.Column(db.Float, nullable=False)
    emissao_evitar = db.Column(db.Float)  # kg CO2 evitados
    data_simulacao = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('simulacoes', lazy=True))
