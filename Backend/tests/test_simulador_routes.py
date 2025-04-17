import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json

from app import create_app, db
from app.models.simulacao_model import Simulacao

class SimuladorRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_enviar_dados_consumo_sucesso(self):
        data = {
            "consumos_kwh": [100, 120, 110, 130, 115, 125],
            "tarifa_atual": 0.85
        }
        response = self.client.post('/simulador/enviar', json=data)
        self.assertEqual(response.status_code, 202)
        response_json = json.loads(response.get_data(as_text=True))
        self.assertIn('id', response_json)
        self.assertIn('mensagem', response_json)

        with self.app.app_context():
            simulacao = Simulacao.query.get(response_json['id'])
            self.assertIsNotNone(simulacao)
            self.assertEqual(simulacao.consumos_kwh, data['consumos_kwh'])
            self.assertEqual(simulacao.tarifa_atual, data['tarifa_atual'])
            self.assertIsNotNone(simulacao.resultado)
            self.assertIn('consumo_medio_mensal_kwh', simulacao.resultado)
            self.assertIn('num_placas_necessarias', simulacao.resultado)
            self.assertIn('economia_anual_estimada_reais', simulacao.resultado)
            self.assertIn('vpl_reais', simulacao.resultado)

    def test_enviar_dados_consumo_invalido_meses(self):
        data_invalida = {
            "consumos_kwh": [100, 120, 110, 130, 115],
            "tarifa_atual": 0.85
        }
        response = self.client.post('/simulador/enviar', json=data_invalida)
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.get_data(as_text=True))
        self.assertIn('erro', response_json)
        self.assertIn('Dados de consumo inválidos', response_json['erro'])

    def test_enviar_dados_consumo_invalido_tarifa(self):
        data_invalida = {
            "consumos_kwh": [100, 120, 110, 130, 115, 125],
            "tarifa_atual": 0
        }
        response = self.client.post('/simulador/enviar', json=data_invalida)
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.get_data(as_text=True))
        self.assertIn('erro', response_json)
        self.assertIn('Tarifa atual inválida', response_json['erro'])

    def test_obter_resultado_simulacao_sucesso(self):
        with self.app.app_context():
            data = {
                "consumos_kwh": [100, 120, 110, 130, 115, 125],
                "tarifa_atual": 0.85
            }
            resultado_simulacao = {
                "consumo_medio_mensal_kwh": 116.67,
                "num_placas_necessarias": 3,
                "economia_anual_estimada_reais": 1190.00,
                "vpl_reais": 15000.00
            }
            simulacao = Simulacao(consumos_kwh=data['consumos_kwh'], tarifa_atual=data['tarifa_atual'], resultado=resultado_simulacao)
            db.session.add(simulacao)
            db.session.commit()
            simulacao_id = simulacao.id

        response = self.client.get(f'/simulador/resultado/{simulacao_id}')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_json, resultado_simulacao)

    def test_obter_resultado_simulacao_nao_encontrado(self):
        response = self.client.get('/simulador/resultado/999')
        self.assertEqual(response.status_code, 404)

    def test_obter_resultado_simulacao_em_processamento(self):
        with self.app.app_context():
            data = {
                "consumos_kwh": [100, 120, 110, 130, 115, 125],
                "tarifa_atual": 0.85
            }
            simulacao = Simulacao(consumos_kwh=data['consumos_kwh'], tarifa_atual=data['tarifa_atual'])
            db.session.add(simulacao)
            db.session.commit()
            simulacao_id = simulacao.id

        response = self.client.get(f'/simulador/resultado/{simulacao_id}')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.get_data(as_text=True))
        self.assertIn('mensagem', response_json)
        self.assertEqual(response_json['mensagem'], 'Simulação ainda em processamento ou ocorreu um erro.')

if __name__ == '__main__':
    unittest.main()
