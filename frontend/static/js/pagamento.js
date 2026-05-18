document.getElementById("paymentForm").addEventListener("submit", function(e) {
    const card = document.querySelector("[name='card_number']").value;
    if(card.length !== 16) {
        alert("Número do cartão inválido!");
        e.preventDefault();
    }

    const expiry = document.querySelector("[name='expiry_date']").value;
    const regex = /^(0[1-9]|1[0-2])\/\d{2}$/;
    if(!regex.test(expiry)) {
        alert("Data de validade inválida! Use o formato MM/AA.");
        e.preventDefault();
    }
});

// Partículas animadas
const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const particles = [];

for (let i = 0; i < 80; i++) {
  particles.push({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    radius: Math.random() * 2 + 1,
    dx: (Math.random() - 0.5) * 0.5,
    dy: (Math.random() - 0.5) * 0.5,
  });
}

function drawParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#00aaff";

  particles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fill();

    p.x += p.dx;
    p.y += p.dy;

    if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
    if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
  });

  requestAnimationFrame(drawParticles);
}

drawParticles();

document.getElementById("paymentForm").addEventListener("submit", function(e) {
    const cvv = document.querySelector("[name='cvv']").value;
    if(!/^\d{3}$/.test(cvv)) {
        alert("CVV inválido!");
        e.preventDefault();
    }
});
