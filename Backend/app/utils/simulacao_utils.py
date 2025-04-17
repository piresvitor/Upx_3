import numpy as np

# Dados de irradiação solar média anual para uma localização hipotética (kWh/m²/ano)
IRRADIACAO_ANUAL = 1500

# Perdas do sistema (%)
PERDAS_SISTEMA = 0.20

# Potência de uma placa solar típica (kWp)
POTENCIA_PLACA = 0.4

# Custo estimado por kWp instalado (R$)
CUSTO_POR_KWP = 5000

# Vida útil do sistema (anos)
VIDA_UTIL = 25

# Taxa de desconto anual (%)
TAXA_DESCONTO = 0.05

def calcular_simulacao(consumos_kwh, tarifa_atual):
    consumo_medio_mensal = np.mean(consumos_kwh)
    consumo_anual = consumo_medio_mensal * 12

    # Cálculo do número de placas necessárias
    energia_placa_anual = POTENCIA_PLACA * IRRADIACAO_ANUAL * (1 - PERDAS_SISTEMA)
    num_placas_necessarias = np.ceil(consumo_anual / energia_placa_anual)

    # Cálculo da potência total instalada
    potencia_total_instalada = num_placas_necessarias * POTENCIA_PLACA

    # Cálculo do custo estimado do sistema
    custo_sistema = potencia_total_instalada * CUSTO_POR_KWP

    # Cálculo da economia anual estimada
    economia_anual = consumo_anual * tarifa_atual

    # Cálculo simplificado do payback
    payback = custo_sistema / economia_anual if economia_anual > 0 else float('inf')

    # Análise de fluxo de caixa simplificada (sem considerar aumento de tarifa ou manutenção)
    fluxo_caixa_anual = economia_anual
    vpl = -custo_sistema
    for ano in range(1, VIDA_UTIL + 1):
        vpl += fluxo_caixa_anual / (1 + TAXA_DESCONTO)**ano

    return {
        "consumo_medio_mensal_kwh": consumo_medio_mensal,
        "consumo_anual_kwh": consumo_anual,
        "num_placas_necessarias": int(num_placas_necessarias),
        "potencia_total_instalada_kwp": round(potencia_total_instalada, 2),
        "custo_estimado_sistema_reais": round(custo_sistema, 2),
        "economia_anual_estimada_reais": round(economia_anual, 2),
        "payback_anos": round(payback, 2) if payback != float('inf') else "Infinito",
        "vpl_reais": round(vpl, 2)
    }
