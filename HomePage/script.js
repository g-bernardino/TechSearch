function scrollBanner(direction) {
    const slider = document.getElementById('bannerSlider');
    const scrollAmount = slider.clientWidth * 0.8; 
    
    if (direction === 1) {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    }
}

function mostrarCupons() {
    var x = document.getElementById("sessao-cupons");
    
    if (x.style.display === "none" || x.style.display === "") {
        x.style.display = "flex";
    } else {
        x.style.display = "none";
    }
}
function copiarCupom(codigo) {
    navigator.clipboard.writeText(codigo).then(() => {
    
        alert("Cupom " + codigo + " copiado! Use no carrinho.");
    });
}

function toggleSuporte() {
    const balao = document.getElementById("suporte-balao");
    
    
    if (balao.style.display === "none") {
        balao.style.display = "block";
    } else {
        balao.style.display = "none";
    }
}
window.addEventListener('click', function(event) {
    const balao = document.getElementById("suporte-balao");
    const icone = document.getElementById("icone-suporte");
    
    if (event.target !== icone && !balao.contains(event.target)) {
        balao.style.display = "none";
    }
});
/* --- ACESSIBILIDADE --- */

// 1. Função para abrir e fechar o menu de acessibilidade
function toggleAcessibilidade() {
    const balao = document.getElementById("acessibilidade-balao");
    
    if (balao.style.display === "none" || balao.style.display === "") {
        balao.style.display = "block";
    } else {
        balao.style.display = "none";
    }
}

// 2. Função para aumentar a fonte (Liga/Desliga)
function toggleFonteAcessivel() {
    // Adiciona ou remove a classe 'fonte-acessivel' do <body>
    document.body.classList.toggle("fonte-acessivel");
}

// 3. Função para o Alto Contraste (Liga/Desliga)
function toggleLuzAcessivel() {
    // Adiciona ou remove a classe 'luz-acessivel' do <body>
    document.body.classList.toggle("luz-acessivel");
}