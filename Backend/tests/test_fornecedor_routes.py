import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db  # Importe db diretamente de app
from app.models.fornecedor_model import Fornecedor

class FornecedorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            fornecedor = Fornecedor(
                nome="SolarTech",
                email="contato@solartech.com",
                telefone="11999999999",
                cidade="São Paulo",
                estado="SP"
            )
            db.session.add(fornecedor)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_lista_fornecedores(self):
        response = self.client.get('/fornecedores/lista')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.get_json()) >= 1)

    def test_solicitar_contato_sucesso(self):
        response = self.client.post('/fornecedores/contato', json={
            'nome': 'Cliente Teste',
            'email': 'cliente@example.com',
            'mensagem': 'Quero instalar energia solar'
        })
        self.assertEqual(response.status_code, 200)

    def test_solicitar_contato_erro(self):
        response = self.client.post('/fornecedores/contato', json={
            'nome': '',
            'email': '',
            'mensagem': ''
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
