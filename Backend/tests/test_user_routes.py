import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user_model import User
from app.utils.jwt_manager import generate_token

class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SECRET_KEY'] = 'sua_chave_secreta' # Importante para gerar o token
        self.client = self.app.test_client()
        self.user_id_teste = None
        self.token_teste = None

        with self.app.app_context():
            db.create_all()
            # Criar um usuário de teste
            user = User(nome="Teste User", email="teste@example.com")
            user.set_password("senha123")
            db.session.add(user)
            db.session.commit()
            self.user_id_teste = user.id
            self.token_teste = generate_token(user.id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_auth_header(self):
        return {'Authorization': f'Bearer {self.token_teste}'}

    def test_obter_dados_usuario_sucesso(self):
        response = self.client.get('/usuario/dados', headers=self.get_auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['id'], self.user_id_teste)
        self.assertIn('nome', data)
        self.assertIn('email', data)

    def test_obter_dados_usuario_erro_token_ausente(self):
        response = self.client.get('/usuario/dados')
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertIn('Token de autenticação não fornecido.', data['erro'])

    def test_obter_dados_usuario_erro_token_invalido(self):
        response = self.client.get('/usuario/dados', headers={'Authorization': 'Bearer header.payload'}) # Estrutura incompleta
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertIn('Token de autenticação inválido.', data['erro'])

    def test_editar_usuario_sucesso(self):
        response = self.client.put('/usuario/editar', headers=self.get_auth_header(), json={
            'nome': 'Novo Nome',
            'email': 'novo@example.com'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('mensagem', data)

        with self.app.app_context():
            updated_user = User.query.get(self.user_id_teste)
            self.assertEqual(updated_user.nome, 'Novo Nome')
            self.assertEqual(updated_user.email, 'novo@example.com')

    def test_editar_usuario_erro_email_existente(self):
        # Criar outro usuário com um email diferente
        with self.app.app_context():
            outro_usuario = User(nome="Outro User", email="outro@example.com")
            outro_usuario.set_password("outrasenha")
            db.session.add(outro_usuario)
            db.session.commit()

        response = self.client.put('/usuario/editar', headers=self.get_auth_header(), json={
            'email': 'outro@example.com'
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertIn('Este email já está em uso.', data['erro'])

    def test_editar_usuario_erro_sem_dados(self):
        response = self.client.put('/usuario/editar', headers=self.get_auth_header(), json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertIn('Nenhum dado fornecido para atualização.', data['erro'])

    def test_deletar_usuario_sucesso(self):
        response = self.client.delete('/usuario/deletar', headers=self.get_auth_header())
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('mensagem', data)

        with self.app.app_context():
            deleted_user = User.query.get(self.user_id_teste)
            self.assertIsNone(deleted_user)

    def test_deletar_usuario_erro_token_ausente(self):
        response = self.client.delete('/usuario/deletar')
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertIn('Token de autenticação não fornecido.', data['erro'])

    def test_deletar_usuario_erro_token_invalido(self):
        response = self.client.delete('/usuario/deletar', headers={'Authorization': 'Bearer token_invalido'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('erro', data)
        self.assertIn('Token de autenticação inválido.', data['erro'])

if __name__ == '__main__':
    unittest.main()
