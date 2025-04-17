from flask import request, jsonify
from app import db
from app.models.simulacao_model import Simulacao
from app.utils.simulacao_utils import calcular_simulacao

def enviar_dados_consumo():
    data = request.get_json()
    consumos_kwh = data.get('consumos_kwh')
    tarifa_atual = data.get('tarifa_atual')

    if not consumos_kwh or not isinstance(consumos_kwh, list) or len(consumos_kwh) != 6 or not all(isinstance(c, (int, float)) for c in consumos_kwh):
        return jsonify({"erro": "Dados de consumo inválidos. Forneça uma lista de 6 valores numéricos (kWh)."}), 400

    if not isinstance(tarifa_atual, (int, float)) or tarifa_atual <= 0:
        return jsonify({"erro": "Tarifa atual inválida."}), 400

    simulacao = Simulacao(consumos_kwh=consumos_kwh, tarifa_atual=tarifa_atual)
    db.session.add(simulacao)
    db.session.commit()

    # Iniciar o cálculo da simulação (pode ser assíncrono em produção)
    resultado = calcular_simulacao(consumos_kwh, tarifa_atual)
    simulacao.resultado = resultado
    db.session.commit()

    return jsonify({"id": simulacao.id, "mensagem": "Dados recebidos e simulação iniciada."}), 202

def obter_resultado_simulacao(simulacao_id):
    simulacao = Simulacao.query.get_or_404(simulacao_id)
    if simulacao.resultado:
        return jsonify(simulacao.resultado), 200
    else:
        return jsonify({"mensagem": "Simulação ainda em processamento ou ocorreu um erro."}), 200
