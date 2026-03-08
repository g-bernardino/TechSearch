function scrollBanner(direction) {
    const slider = document.getElementById('bannerSlider');
    const scrollAmount = slider.clientWidth * 0.8; 
    
    if (direction === 1) {
        slider.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    } else {
        slider.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    }
}