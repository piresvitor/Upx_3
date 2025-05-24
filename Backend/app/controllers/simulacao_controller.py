from flask import request, jsonify
from app import db
from app.models.simulacao_model import Simulacao
from app.models.user_model import User
from app.utils.simulacao_utils import calcular_simulacao

def enviar_dados_consumo(user_email):
    data = request.get_json()
    consumos_kwh = data.get('consumos_kwh')
    tarifa_atual = data.get('tarifa_atual')

    # Validações
    if not consumos_kwh or not isinstance(consumos_kwh, list) or len(consumos_kwh) != 6 or not all(isinstance(c, (int, float)) for c in consumos_kwh):
        return jsonify({"erro": "Dados de consumo inválidos. Forneça uma lista de 6 valores numéricos (kWh)."}), 400

    if not isinstance(tarifa_atual, (int, float)) or tarifa_atual <= 0:
        return jsonify({"erro": "Tarifa atual inválida."}), 400

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    simulacao = Simulacao(
        user_id=user.id,
        consumos_kwh=consumos_kwh,
        tarifa_atual=tarifa_atual
    )
    db.session.add(simulacao)
    db.session.commit()

    resultado = calcular_simulacao(consumos_kwh, tarifa_atual)
    simulacao.resultado = resultado
    db.session.commit()

    return jsonify({"id": simulacao.id, "mensagem": "Dados recebidos e simulação iniciada."}), 202

def obter_resultado_simulacao(simulacao_id, user_email):
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    simulacao = Simulacao.query.filter_by(id=simulacao_id, user_id=user.id).first()
    if not simulacao:
        return jsonify({"erro": "Simulação não encontrada para este usuário."}), 404

    if simulacao.resultado:
        return jsonify(simulacao.resultado), 200
    else:
        return jsonify({"mensagem": "Simulação ainda em processamento ou ocorreu um erro."}), 200

def listar_simulacoes_usuario(user_email):
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    simulacoes = Simulacao.query.filter_by(user_id=user.id).all()

    lista = []
    for simu in simulacoes:
        lista.append({
            "id": simu.id,
            "consumo_medio_mensal_kwh": getattr(simu.resultado, 'consumo_medio_mensal_kwh', None),
            "data_criacao": simu.data_envio.strftime("%Y-%m-%d %H:%M:%S") if simu.data_envio else None,
            "status": getattr(simu, 'status', 'Concluída')  # ajuste se status existe
        })

    return jsonify(lista)