$(document).ready(function(){
    $('#mobile_btn').on('click', function(){
        $('#mobile_menu').toggleClass('active');
        $('#mobile_btn').find('i').toggleClass('fa-x');
    });

    const sections = $('section');
    const navItems = $(".nav-item")

    $(window).on('scroll', function(){
        const header = $('header');
        const scrollPosition = $(window).scrollTop() - header.outerHeight();

        let activeSectionIndex = 0;


        if (scrollPosition <= 0){
            header.css('box-shadow', 'none');
        } else{
            header.css('box-shadow', '5px 1px 5px rgba(0, 0, 0, 0.1)');
        }

        sections.each(function(i){
            const section = $(this);
            const sectionTop = section.offset().top - 96;
            const sectionBottom = sectionTop + section.outerHeight();

            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom){
                activeSectionIndex = i;
                return false;
            }
        });

        navItems.removeClass('active');
        $(navItems[activeSectionIndex]).addClass('active');

    });

    ScrollReveal().reveal('#cta', {
        origin: 'left',
        duration: 2000,
        distance: '20%'
    });

    ScrollReveal().reveal('.dish', {
        origin: 'left',
        duration: 2000,
        distance: '20%'
    });

    ScrollReveal().reveal('#testimonial_aval', {
        origin: 'left',
        duration: 1000,
        distance: '20%'
    })

    ScrollReveal().reveal('.feedback', {
        origin: 'right',
        duration: 1000,
        distance: '20%'
    })

    ScrollReveal().reveal('.footer', {
        origin: 'bottom',
        duration: 2000,
        distance: '20%'
    })

      // Modal controls
  const $modalLogin = $('#modal-login');
  const $modalCadastro = $('#modal-cadastro');

  // Abrir modal login
  $('button.btn-default:contains("Login"), #cta_buttons a:contains("Login")').click(function(e){
    e.preventDefault();
    $modalLogin.removeClass('hidden');
  });

  // Abrir modal cadastro
  $('a:contains("Cadastre-se")').click(function(e){
    e.preventDefault();
    $modalCadastro.removeClass('hidden');
  });

  // Fechar modais
  $('#close-login').click(() => $modalLogin.addClass('hidden'));
  $('#close-cadastro').click(() => $modalCadastro.addClass('hidden'));

  // Switch modais
  $('#to-register').click(e => {
    e.preventDefault();
    $modalLogin.addClass('hidden');
    $modalCadastro.removeClass('hidden');
  });
  $('#to-login').click(e => {
    e.preventDefault();
    $modalCadastro.addClass('hidden');
    $modalLogin.removeClass('hidden');
  });

  // URL base da API - ajuste se necessário
  const API_BASE = 'http://localhost:5000';

  // Função para salvar token no localStorage
  function saveToken(token){
    localStorage.setItem('token', token);
  }

  // Login
  $('#form-login').submit(function(e){
    e.preventDefault();
    const email = $('#login-email').val();
    const senha = $('#login-senha').val();

    $.ajax({
      url: `${API_BASE}/auth/login`,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({email, senha}),
      success: function(response){
        alert('Login efetuado com sucesso!');
        saveToken(response.token);
        $modalLogin.addClass('hidden');
        // Redireciona para o dashboard
        window.location.href = "dashboard.html";
      },
      error: function(xhr){
        alert(`Erro no login: ${xhr.responseJSON?.erro || 'Desconhecido'}`);
      }
    });
  });

  // Cadastro
  $('#form-cadastro').submit(function(e){
    e.preventDefault();
    const nome = $('#cadastro-nome').val();
    const email = $('#cadastro-email').val();
    const senha = $('#cadastro-senha').val();

    $.ajax({
      url: `${API_BASE}/auth/cadastro`,
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({nome, email, senha}),
      success: function(response){
        alert('Cadastro realizado com sucesso! Faça login.');
        $modalCadastro.addClass('hidden');
        $modalLogin.removeClass('hidden');
      },
      error: function(xhr){
        alert(`Erro no cadastro: ${xhr.responseJSON?.erro || 'Desconhecido'}`);
      }
    });
  });
});
