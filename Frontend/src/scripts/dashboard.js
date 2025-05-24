$(document).ready(function(){
  const API_BASE = 'http://localhost:5000';

  // Token helpers
  function getToken() {
    return localStorage.getItem('token');
  }
  
  function handleUnauthorized() {
    alert('Sessão expirada ou não autenticado. Faça login novamente.');
    localStorage.removeItem('token');
    window.location.href = 'index.html';
  }
  
  function ajaxAuthHeaders() {
    const token = getToken();
    if (!token) {
      handleUnauthorized();
      return null;
    }
    return { 'Authorization': 'Bearer ' + token };
  }

  // Tab switching
  $('.tab-btn').click(function() {
    const tab = $(this).data('tab');
    $('.tab-btn').removeClass('active');
    $(this).addClass('active');
    $('.tab-content').removeClass('active').hide();
    $('#' + tab).addClass('active').show();
    if (tab === 'visualizar') {
      carregarSimulacoes();
    }
  });

  // Logout button
  $('#btn-logout').click(function() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
  });

  // Carregar dados do usuário
  function carregarDadosUsuario() {
    const headers = ajaxAuthHeaders();
    if (!headers) return;
    $.ajax({
      url: `${API_BASE}/usuario/dados`,
      method: 'GET',
      headers: headers,
      success: function(data) {
        $('#user-nome').text(data.nome);
        $('#user-email').text(data.email);
      },
      error: function(xhr) {
        if (xhr.status === 401) {
          handleUnauthorized();
        } else {
          alert('Erro ao carregar dados do usuário.');
        }
      }
    });
  }
  carregarDadosUsuario();

  // Enviar simulação
  $('#form-simulacao').submit(function(e){
    e.preventDefault();
    $('#simulacao-sucesso').hide();
    $('#simulacao-erro').hide();

    const headers = ajaxAuthHeaders();
    if (!headers) return;

    const consumosStr = $('#input-consumos').val();
    const consumos = consumosStr.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
    const tarifa = parseFloat($('#input-tarifa').val());

    if (consumos.length !== 6) {
      $('#simulacao-erro').text('Informe exatamente 6 valores de consumo.').show();
      return;
    }
    if (isNaN(tarifa) || tarifa <= 0) {
      $('#simulacao-erro').text('Informe uma tarifa válida.').show();
      return;
    }

    $.ajax({
      url: `${API_BASE}/simulador/enviar`,
      method: 'POST',
      headers: headers,
      contentType: 'application/json',
      data: JSON.stringify({ consumos_kwh: consumos, tarifa_atual: tarifa }),
      success: function(resp){
        $('#simulacao-sucesso').text(`Simulação enviada com sucesso! ID: ${resp.id}`).show();
      },
      error: function(xhr){
        if (xhr.status === 401) {
          handleUnauthorized();
        } else {
          $('#simulacao-erro').text(xhr.responseJSON?.erro || 'Erro desconhecido ao enviar simulação.').show();
        }
      }
    });
  });

  // Carregar lista de simulações
  function carregarSimulacoes() {
    $('#lista-simulacoes').html('<p>Carregando simulações...</p>');
    $('#detalhes-simulacao').hide();
    $('#visualizacao-erro').hide();

    const headers = ajaxAuthHeaders();
    if (!headers) return;

    $.ajax({
      url: `${API_BASE}/simulador/lista`,
      method: 'GET',
      headers: headers,
      success: function(data) {
        if (data.length === 0) {
          $('#lista-simulacoes').html('<p>Nenhuma simulação encontrada.</p>');
          return;
        }
        let html = '<ul>';
        data.forEach(simulacao => {
          html += `<li><button class="btn-simulacao" data-id="${simulacao.id}">Simulação #${simulacao.id} - Enviada em ${simulacao.data_criacao || 'N/A'}</button></li>`;
        });
        html += '</ul>';
        $('#lista-simulacoes').html(html);

        $('.btn-simulacao').off('click').click(function() {
          const id = $(this).data('id');
          carregarDetalhesSimulacao(id);
        });
      },
      error: function(xhr) {
        if (xhr.status === 401) {
          handleUnauthorized();
        } else {
          $('#lista-simulacoes').html('<p>Erro ao carregar simulações.</p>');
        }
      }
    });
  }

  // Carregar detalhes de simulação (tabela + gráfico)
  let chartInstance = null;
  let projecoesChart = null;

  function carregarDetalhesSimulacao(id) {
    $('#detalhes-simulacao').hide();
    $('#visualizacao-erro').hide();

    const headers = ajaxAuthHeaders();
    if (!headers) return;

    $.ajax({
      url: `${API_BASE}/simulador/resultado/${id}`,
      method: 'GET',
      headers: headers,
      success: function(data) {
        $('#simulacao-id').text(id);
        const tbody = $('#tabela-simulacao tbody').empty();

        const campos = [
          "consumo_medio_mensal_kwh",
          "consumo_anual_kwh",
          "num_placas_necessarias",
          "potencia_total_instalada_kwp",
          "custo_estimado_sistema_reais",
          "economia_anual_estimada_reais",
          "payback_anos",
          "vpl_reais"
        ];

        let linha = '<tr>';
        campos.forEach(campo => {
          let valor = data[campo];
          if (valor !== undefined && typeof valor === 'number') {
            if (campo.includes('reais'))
              valor = valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
            else
              valor = valor.toFixed(2);
          }
          linha += `<td>${valor !== undefined ? valor : '-'}</td>`;
        });
        linha += '</tr>';
        tbody.append(linha);

        $('#detalhes-simulacao').show();

        montarGrafico(data);
        montarGraficoProjecoes();
      },
      error: function(xhr) {
        if (xhr.status === 401) {
          handleUnauthorized();
        } else {
          $('#visualizacao-erro').text(xhr.responseJSON?.erro || 'Erro ao obter detalhes da simulação.').show();
        }
      }
    });
  }

  // Montar gráfico com Chart.js - dados da simulação
  function montarGrafico(data) {
    if (chartInstance) chartInstance.destroy();

    if (typeof Chart === 'undefined') {
      $.getScript('https://cdn.jsdelivr.net/npm/chart.js', function() {
        criarGrafico(data);
      });
    } else {
      criarGrafico(data);
    }
  }

  function criarGrafico(data) {
    const ctx = $('#chart-simulacao');

    const labels = ['Consumo Médio (kWh)', 'Consumo Anual (kWh)', 'Economia Anual (R$)'];
    const valores = [
      data.consumo_medio_mensal_kwh || 0,
      data.consumo_anual_kwh || 0,
      data.economia_anual_estimada_reais || 0
    ];

    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Valores',
          data: valores,
          backgroundColor: ['#FB820C', '#FEBF63', '#82C91E']
        }]
      },
      options: {
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }

  // Montar gráfico de projeções - exemplo simples
  function montarGraficoProjecoes() {
    if (projecoesChart) projecoesChart.destroy();

    const ctx = document.getElementById('chart-projecoes').getContext('2d');

    const labels = ['2025', '2026', '2027', '2028', '2029', '2030'];
    const economiaProjetada = [0, 1500, 3000, 4500, 6000, 7500];
    const reducaoCO2 = [0, 1.2, 2.5, 3.7, 5.0, 6.2];

    projecoesChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Economia acumulada (R$)',
            data: economiaProjetada,
            borderColor: '#FC840B',
            backgroundColor: 'rgba(252,132,11,0.3)',
            yAxisID: 'y',
            fill: true,
            tension: 0.3,
          },
          {
            label: 'Redução de CO₂ (toneladas)',
            data: reducaoCO2,
            borderColor: '#1d891d',
            backgroundColor: 'rgba(29,137,29,0.3)',
            yAxisID: 'y1',
            fill: true,
            tension: 0.3,
          }
        ],
      },
      options: {
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            title: { display: true, text: 'Economia (R$)' },
            beginAtZero: true
          },
          y1: {
            type: 'linear',
            position: 'right',
            title: { display: true, text: 'Redução CO₂ (toneladas)' },
            beginAtZero: true,
            grid: { drawOnChartArea: false },
          }
        },
        interaction: { mode: 'index', intersect: false },
        plugins: { tooltip: { enabled: true }, legend: { position: 'top' } }
      }
    });
   }
});
