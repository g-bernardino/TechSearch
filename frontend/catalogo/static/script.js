// 1. SCROLL DOS PRODUTOS
function scrollProdutos(direcao) {
    const slider = document.getElementById('produtosSlider');
    // Definimos que cada clique move 300px (tamanho aproximado de um card)
    const scrollAmount = 300; 
    
    if (direcao === 1) {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    }
}

// 2. SCROLL DAS CATEGORIAS
function scrollCategorias(direcao) {
    const slider = document.getElementById('categoriasSlider');
    const scrollAmount = 200;
    
    if (direcao === 1) {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    }
}

// 3. CONTROLO DOS BANNERS (Simples)
function scrollBanner(direcao) {
    const slider = document.getElementById('bannerSlider');
    const width = slider.clientWidth; // Pega a largura visível do banner
    
    if (direcao === 1) {
        slider.scrollBy({ left: width, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -width, behavior: 'smooth' });
    }
}

// 4. INTERATIVIDADE: Ícone de Favorito (Coração)
document.querySelectorAll('.heart-icon').forEach(icon => {
    icon.addEventListener('click', function() {
        if (this.innerHTML === '🤍') {
            this.innerHTML = '❤️';
            this.style.color = '#ff4757';
        } else {
            this.innerHTML = '🤍';
            this.style.color = '';
        }
    });
});