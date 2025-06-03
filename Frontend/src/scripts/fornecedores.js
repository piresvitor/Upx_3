$(document).ready(function(){
  const API_BASE = 'http://localhost:5000';

  // Token helpers
  function getToken() {
    return localStorage.getItem('token');
  }
  function ajaxAuthHeaders() {
    const token = getToken();
    if (!token) {
      alert('Usuário não autenticado. Faça login.');
      window.location.href = 'index.html';
      return null;
    }
    return { 'Authorization': 'Bearer ' + token };
  }

  // Abrir modal contato
  function abrirModalContato(id) {
    $('#fornecedor-id').val(id);
    $('#contato-nome').val('');
    $('#contato-email').val('');
    $('#contato-mensagem').val('');
    $('#mensagem-resultado').html('');
    $('#modal-contato').removeClass('hidden');
  }

  // Fechar modal contato
  $('#close-contato').click(() => {
    $('#modal-contato').addClass('hidden');
  });

  // Buscar lista fornecedores
  function carregarFornecedores() {
    const headers = ajaxAuthHeaders();
    if (!headers) return;

    $('#lista-fornecedores').html('<p>Carregando fornecedores...</p>');
    $.ajax({
      url: `${API_BASE}/fornecedores/lista`,
      method: 'GET',
      headers: headers,
      success: function(data){
        if(!data.length){
          $('#lista-fornecedores').html('<p>Nenhum fornecedor encontrado.</p>');
          return;
        }
        let html = '';
        data.forEach(fornecedor => {
          html += `<div class="fornecedor-card">
            <h3>${fornecedor.nome}</h3>
            <p><i class="fa-solid fa-envelope"></i> ${fornecedor.email}</p>
            <p><i class="fa-solid fa-phone"></i> ${fornecedor.telefone}</p>
            <button class="btn-default btn-contato" data-id="${fornecedor.id}">Entrar em Contato</button>
          </div>`;
        });
        $('#lista-fornecedores').html(html);

        $('.btn-contato').off('click').click(function(){
          abrirModalContato($(this).data('id'));
        });
      },
      error: function(){
        $('#lista-fornecedores').html('<p>Erro ao carregar fornecedores.</p>');
      }
    });
  }
  carregarFornecedores();

  // Enviar contato fornecedor
  $('#form-contato-fornecedor').submit(function(e){
    e.preventDefault();
    const headers = ajaxAuthHeaders();
    if (!headers) return;

    const fornecedor_id = $('#fornecedor-id').val();
    const nome = $('#contato-nome').val().trim();
    const email = $('#contato-email').val().trim();
    const mensagem = $('#contato-mensagem').val().trim();

    if(!nome || !email || !mensagem) {
      $('#mensagem-resultado').html('<span style="color:red;">Preencha todos os campos.</span>');
      return;
    }

    $.ajax({
      url: `${API_BASE}/fornecedores/contato`,
      method: 'POST',
      headers: headers,
      contentType: 'application/json',
      data: JSON.stringify({ fornecedor_id, nome, email, mensagem }),
      success: function(resp){
        $('#mensagem-resultado').html('<span style="color:green;">Pedido de contato enviado com sucesso.</span>');
        setTimeout(() => $('#modal-contato').addClass('hidden'), 3000);
      },
      error: function(xhr){
        $('#mensagem-resultado').html('<span style="color:red;">Erro ao enviar o pedido de contato.</span>');
      }
    });
  });
});