$(document).ready(function(){
  const API_BASE = 'http://localhost:5000';
  const token = localStorage.getItem('token');

  if (!token) {
    alert('Você precisa estar logado para acessar o dashboard.');
    window.location.href = 'index.html';
    return;
  }

  // Função para carregar dados do usuário logado
  function carregarUsuario() {
    $.ajax({
      url: `${API_BASE}/usuario/dados`,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      success: function(data) {
        $('#user-nome').text(data.nome);
        $('#user-email').text(data.email);
      },
      error: function() {
        alert('Erro ao carregar dados do usuário. Faça login novamente.');
        localStorage.removeItem('token');
        window.location.href = 'index.html';
      }
    });
  }

  carregarUsuario();

  // Logout
  $('#btn-logout').click(function() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
  });

  // Enviar simulação
  $('#form-simulacao').submit(function(e) {
    e.preventDefault();

    $('#simulacao-sucesso').hide();
    $('#simulacao-erro').hide();

    let consumosStr = $('#input-consumos').val();
    let consumos = consumosStr.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
    let tarifa = parseFloat($('#input-tarifa').val());

    if (consumos.length !== 6) {
      $('#simulacao-erro').text('Por favor, informe exatamente 6 valores de consumo.').show();
      return;
    }
    if (isNaN(tarifa) || tarifa <= 0) {
      $('#simulacao-erro').text('Informe uma tarifa válida.').show();
      return;
    }

    $.ajax({
      url: `${API_BASE}/simulador/enviar`,
      method: 'POST',
      contentType: 'application/json',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      data: JSON.stringify({
        consumos_kwh: consumos,
        tarifa_atual: tarifa
      }),
      success: function(response) {
        // Espera-se algo com id da simulação no response - seu swagger tinha id no 202
        $('#simulacao-sucesso').text(`Simulação enviada com sucesso! ID da simulação: ${response.id || '(não disponível)'}`).show();
      },
      error: function(xhr) {
        let msg = xhr.responseJSON?.erro || 'Erro desconhecido ao enviar simulação.';
        $('#simulacao-erro').text(msg).show();
      }
    });
  });

  // Consultar resultado da simulação
  $('#form-consulta').submit(function(e) {
    e.preventDefault();

    $('#resultado-simulacao').hide();
    $('#consulta-erro').hide();

    let id = $('#input-id-simulacao').val().trim();
    if (!id) {
      $('#consulta-erro').text('Informe o ID da simulação.').show();
      return;
    }

    $.ajax({
      url: `${API_BASE}/simulador/resultado/${id}`,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      success: function(data) {
        $('#resultado-json').text(JSON.stringify(data, null, 2));
        $('#resultado-simulacao').show();
      },
      error: function(xhr) {
        let msg = xhr.responseJSON?.erro || 'Erro desconhecido ao obter resultado.';
        $('#consulta-erro').text(msg).show();
      }
    });
  });
});