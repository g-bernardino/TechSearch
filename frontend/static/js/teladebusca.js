const data = [
  { title: "Console Sony PlayStation 5", desc: "Topo da página GALERIA ESPECIFI...", img: "ps5.jpg" },
  { title: "Placa de Vídeo RTX 4060 Ti MSI NVIDIA", desc: "Topo da página GALERIA ESPECIFI...", img: "rtx4060ti.jpg" },
  { title: "Teclado Kumara White", desc: "Aprecie a beleza da linha Lunar W...", img: "kumara_white.jpg" },
  { title: "Teclado Kumara RGB", desc: "Teclado mecânico com iluminação RGB", img: "kumara_rgb.jpg" }
];

const input = document.getElementById("searchInput");
const resultsList = document.getElementById("resultsList");
const searchTerm = document.getElementById("searchTerm");

input.addEventListener("input", () => {
  const value = input.value.toLowerCase();
  resultsList.innerHTML = "";
  searchTerm.textContent = value;

  if (value.length === 0) return;

  const filtered = data.filter(item => item.title && item.title.toLowerCase().includes(value));

  if (filtered.length === 0) {
    resultsList.innerHTML = "<li>Nenhum resultado encontrado</li>";
    showPopup("Nenhum resultado encontrado");
    return;
  }

  filtered.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `
      <img src="${item.img}" alt="${item.title}">
      <div>
        <strong>${item.title}</strong><br>
        <span>${item.desc}</span>
      </div>`;
    resultsList.appendChild(li);
  });

  // Exibe pop-up com quantidade de resultados
  showPopup(`Encontramos ${filtered.length} resultado(s) para "${value}"`);
});

// Função para criar o pop-up
function showPopup(message) {
  const popup = document.createElement("div");
  popup.classList.add("popup");
  popup.textContent = message;

  document.body.appendChild(popup);

  // Remove o pop-up depois da animação (~2s)
  setTimeout(() => {
    popup.remove();
  }, 2000);
}
