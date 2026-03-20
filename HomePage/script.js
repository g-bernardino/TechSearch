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
    
    // Se a caixa estiver escondida (none), ela vira visível (flex)
    // Se já estiver visível, ela esconde de novo
    if (x.style.display === "none" || x.style.display === "") {
        x.style.display = "flex";
    } else {
        x.style.display = "none";
    }
}