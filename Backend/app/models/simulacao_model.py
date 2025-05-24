from app import db
from datetime import datetime
from app.models.user_model import User  # para garantir importação e evitar erros

class Simulacao(db.Model):
    __tablename__ = 'simulacoes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id', name='fk_simulacoes_user_id_users'),
    nullable=False
)
    consumos_kwh = db.Column(db.JSON, nullable=False)
    tarifa_atual = db.Column(db.Float, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    resultado = db.Column(db.JSON)

    user = db.relationship('User', backref=db.backref('simulacoes', lazy=True))

    def __repr__(self):
        return f'<Simulacao {self.id}>'