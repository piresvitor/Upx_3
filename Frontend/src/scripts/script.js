$(document).ready(function(){
    // Toggle menu mobile
    $('#mobile_btn').on('click', function(){
        $('#mobile_menu').toggleClass('active');
        $('#mobile_btn').find('i').toggleClass('fa-x');
    });

    const sections = $('section');
    const navItems = $(".nav-item");

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
    });

    ScrollReveal().reveal('.feedback', {
        origin: 'right',
        duration: 1000,
        distance: '20%'
    });

    ScrollReveal().reveal('.footer', {
        origin: 'bottom',
        duration: 2000,
        distance: '20%'
    });

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

    // Funções para token JWT
    function saveToken(token){
        localStorage.setItem('token', token);
    }

    function getToken(){
        return localStorage.getItem('token');
    }

    function ajaxAuthHeaders() {
        const token = getToken();
        if (!token) {
            alert('Usuário não autenticado! Faça login.');
            window.location.href = 'index.html';
            return null;
        }
        return { 'Authorization': 'Bearer ' + token };
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

    // Logout
    $('#btn-logout').click(function(){
        localStorage.removeItem('token');
        window.location.href = 'index.html';
    });

    // Função para carregar dados do usuário logado - para dashboard.html
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
                alert('Erro ao carregar dados do usuário. Faça login novamente.');
                localStorage.removeItem('token');
                window.location.href = 'index.html';
            }
        });
    }

    // Exemplo para envio de simulação
    $('#form-simulacao').submit(function(e){
        e.preventDefault();
        const headers = ajaxAuthHeaders();
        if(!headers) return;

        const consumosStr = $('#input-consumos').val();
        const consumos = consumosStr.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
        const tarifa = parseFloat($('#input-tarifa').val());

        if(consumos.length !== 6) {
            alert('Informe exatamente 6 valores de consumo.');
            return;
        }
        if(isNaN(tarifa) || tarifa <= 0){
            alert('Informe uma tarifa válida.');
            return;
        }

        $.ajax({
            url: `${API_BASE}/simulador/enviar`,
            method: 'POST',
            headers: headers,
            contentType: 'application/json',
            data: JSON.stringify({consumos_kwh: consumos, tarifa_atual: tarifa}),
            success: function(resp){
                alert(`Simulação enviada com sucesso! ID: ${resp.id}`);
            },
            error: function(xhr){
                alert(`Erro ao enviar simulação: ${xhr.responseJSON?.erro || 'Erro desconhecido'}`);
            }
        });
    });

    // Ao carregar página dashboard.html, tenta buscar dados do usuário
    if(window.location.pathname.includes('dashboard.html')){
        carregarDadosUsuario();
        // Aqui você pode chamar outras funções para carregar simulações e detalhes
    }
});
