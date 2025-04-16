from app import db

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    cidade = db.Column(db.String(80))
    estado = db.Column(db.String(2))

    def __repr__(self):
        return f'<Fornecedor {self.nome}>'
