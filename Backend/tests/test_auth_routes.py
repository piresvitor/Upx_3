import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import create_app
from app.models.user_model import db

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # banco em memória para teste
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_cadastro(self):
        response = self.client.post('/auth/cadastro', json={
            'nome': 'Maria Teste',
            'email': 'maria@example.com',
            'senha': '123456'
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        # Primeiro cria usuário
        self.client.post('/auth/cadastro', json={
            'nome': 'João',
            'email': 'joao@example.com',
            'senha': 'senha123'
        })
        # Agora testa login
        response = self.client.post('/auth/login', json={
            'email': 'joao@example.com',
            'senha': 'senha123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_logout(self):
        response = self.client.get('/auth/logout')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
