function scrollBanner(direction) {
    const slider = document.getElementById('bannerSlider');
    const scrollAmount = slider.clientWidth * 0.8; 
    
    if (direction === 1) {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    }
}

window.addEventListener("DOMContentLoaded", () => {
  const logado = localStorage.getItem("techsearchLogged");
  const usuario = JSON.parse(localStorage.getItem("techsearchUser"));

  if (logado === "true" && usuario) {
    document.getElementById("header-auth").innerHTML = `
      <span>Bem-vindo, ${usuario.usuario}</span>
      <a href="#" id="logout">Sair</a>
    `;

    document.getElementById("logout").addEventListener("click", () => {
      localStorage.removeItem("techsearchLogged");
      window.location.href = "index.html";
    });
  }
});

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

/**
 * DECLARAÇÃO DE ESTADO
 * Armazena os nomes dos produtos em arrays para permitir a listagem 
 * e evitar duplicatas na interface.
 */
let listaCarrinho = [];
let listaFavoritos = [];

/**
 * FUNÇÃO DE ATUALIZAÇÃO DE INTERFACE (UI)
 * Esta função é responsável por limpar as mensagens de "Vazio" e injetar
 * os nomes dos produtos dentro das divs de visualização no topo do site.
 */
function atualizarBalao(tipo) {
    const lista = (tipo === 'carrinho') ? listaCarrinho : listaFavoritos;
    const divBalao = document.getElementById(`lista-${tipo}-display`);
    const contador = document.getElementById(`cont-${tipo}`);

    // Atualiza o contador numérico visual no ícone
    contador.innerText = lista.length;

    // Condicional: Se a lista estiver vazia, restaura a mensagem padrão
    if (lista.length === 0) {
        divBalao.innerHTML = `<p>${tipo === 'carrinho' ? 'Carrinho vazio' : 'Nenhum favorito'}</p>`;
        return;
    }

    // Renderização Dinâmica: Limpa o conteúdo e mapeia a lista para elementos HTML
    divBalao.innerHTML = ""; 
    lista.forEach(item => {
        divBalao.innerHTML += `<div class="item-lista">${item}</div>`;
    });
}

/**
 * FUNÇÃO: ADICIONAR AO CARRINHO
 * Recebe o nome do produto como parâmetro, verifica se ele já existe na lista
 * para evitar repetição e dispara a atualização do balão visual.
 */
function adicionarAoCarrinho(nomeDoProduto) {
    if (!listaCarrinho.includes(nomeDoProduto)) {
        listaCarrinho.push(nomeDoProduto);
        atualizarBalao('carrinho');
        alert(nomeDoProduto + " adicionado com sucesso!");
    } else {
        alert("Atenção: Este produto já consta no seu carrinho.");
    }
}

/**
 * FUNÇÃO: TOGGLE LIKE (FAVORITOS)
 * Gerencia a entrada e saída de produtos na lista de favoritos.
 * Utiliza o estado da classe 'ativo' no botão para decidir entre adicionar ou remover.
 */
function toggleLike(botao, nomeDoProduto) {
    if (botao.classList.contains("ativo")) {
        // Fluxo de Remoção: Filtra a lista removendo o item específico
        botao.classList.remove("ativo");
        listaFavoritos = listaFavoritos.filter(item => item !== nomeDoProduto);
    } else {
        // Fluxo de Adição: Inclui o item caso não esteja presente
        botao.classList.add("ativo");
        if (!listaFavoritos.includes(nomeDoProduto)) {
            listaFavoritos.push(nomeDoProduto);
        }
    }
    atualizarBalao('favoritos');
}

// Abre a caixinha de digitar
function abrirInputCep() {
    document.getElementById('cep-link').style.display = 'none';
    document.getElementById('cep-input-container').style.display = 'inline-flex';
}

// 1. Função que roda assim que o site abre para ver se já tem um CEP salvo
window.onload = function() {
    const cepSalvo = localStorage.getItem('user-cep');
    if (cepSalvo) {
        document.getElementById('cep-link').innerText = cepSalvo;
    }
}

// 2. Abre a caixinha de digitar
function abrirInputCep() {
    document.getElementById('cep-link').style.display = 'none';
    document.getElementById('cep-input-container').style.display = 'inline-flex';
}

// 3. Salva o CEP no navegador e atualiza a tela
function confirmarCep() {
    const input = document.getElementById('cep-novo');
    const link = document.getElementById('cep-link');
    const container = document.getElementById('cep-input-container');

    if (input.value.trim() !== "") {
        const novoCep = input.value;
        
        // O SEGREDO: Salva na "gavetinha" do navegador
        localStorage.setItem('user-cep', novoCep);
        
        link.innerText = novoCep;
        container.style.display = 'none';
        link.style.display = 'inline';
    } else {
        alert("Digite um CEP válido!");
    }
}
