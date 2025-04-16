from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ConsumoEnergia(db.Model):
    __tablename__ = 'consumo_energia'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mes_referencia = db.Column(db.String(7), nullable=False)  # Ex: "2024-11"
    consumo_kwh = db.Column(db.Float, nullable=False)
    valor_conta = db.Column(db.Float, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('consumos', lazy=True))
