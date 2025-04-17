import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import create_app
from app.models.user_model import db



class SimuladorRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        # Define uma rota de teste diretamente na aplicação
        @self.app.route('/teste')
        def teste_rota():
            return "Rota de teste funcionando", 200

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_rota_de_teste(self):
        response = self.client.get('/teste')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Rota de teste funcionando")

if __name__ == '__main__':
    unittest.main()
