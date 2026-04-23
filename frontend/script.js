function scrollBanner(direction) {
    const slider = document.getElementById('bannerSlider');
    const scrollAmount = slider.clientWidth * 0.8; 
    
    if (direction === 1) {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    }
}

function scrollCategorias(direction) {
    const slider = document.getElementById('categoriasSlider');
    const scrollAmount = 200;

    slider.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth'
    });
}

function scrollProdutos(direction) {
    const slider = document.getElementById('produtosSlider');
    const scrollAmount = 250; 
    slider.scrollBy({
        left: direction * scrollAmount,
        behavior: 'smooth'
    });
}