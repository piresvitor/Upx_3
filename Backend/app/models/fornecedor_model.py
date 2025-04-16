from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FornecedorSolar(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cidade = db.Column(db.String(50))
    site = db.Column(db.String(255))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
