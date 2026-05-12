let cartCount = 0;
/* ===== TOAST ===== */
function showToast(msg) {
    const toast = document.getElementById('toast');
    document.getElementById('toastMsg').textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}
/* ===== CARRINHO ===== */
function addCart(btn) {
    cartCount++;
    document.querySelector('.cart-badge').textContent = cartCount;
    const name = btn.closest('.product-card').querySelector('.product-name').textContent;
    showToast(`"${name.slice(0, 28)}..." adicionado!`);
}
/* ===== FAVORITOS ===== */
function toggleWish(el) {
    el.classList.toggle('active');
    const icon = el.querySelector('i');
    if (el.classList.contains('active')) {
        icon.classList.replace('far', 'fas');
        showToast('Adicionado aos favoritos ❤️');
    } else {
        icon.classList.replace('fas', 'far');
    }
}
/* ===== FILTRO DE CATEGORIAS ===== */
function filterCat(chip, cat) {
    document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    document.querySelectorAll('.product-card').forEach(card => {
        if (cat === 'all' || card.dataset.cat === cat) {
            card.style.display = '';
            card.style.animation = 'fadeInUp 0.3s ease both';
        } else {
            card.style.display = 'none';
        }
    });
}
/* ===== CUPOM ===== */
function copyCode() {
    navigator.clipboard.writeText('TECH10').then(() => {
        showToast('Cupom TECH10 copiado! 🎉');
    });
}
/* ===== NEWSLETTER ===== */
function subscribeNewsletter(e) {
    e.preventDefault();
    showToast('Inscrição realizada com sucesso! 🎉');
    e.target.reset();
}
