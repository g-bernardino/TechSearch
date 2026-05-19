document.addEventListener('DOMContentLoaded', () => {
    const radioCartao = document.getElementById('radioCartao');
    const radioPix = document.getElementById('radioPix');
    const radioBoleto = document.getElementById('radioBoleto');
    
    const cardFields = document.getElementById('cardFields');
    
    if (!cardFields) return; // Segurança caso o elemento não exista na página
    const cardInputs = cardFields.querySelectorAll('input');

    function atualizarFormulario() {
        if (radioCartao && radioCartao.checked) {
            // Se for CARTÃO: mostra os campos e obriga o preenchimento
            cardFields.classList.remove('hidden');
            cardInputs.forEach(input => {
                input.setAttribute('required', 'true');
            });
        } else {
            // Se for PIX ou BOLETO: esconde os campos e livra a obrigatoriedade
            cardFields.classList.add('hidden');
            cardInputs.forEach(input => {
                input.removeAttribute('required');
                input.value = ''; // Limpa os dados digitados
            });
        }
    }

    // Escutar as mudanças de opção
    if (radioCartao) radioCartao.addEventListener('change', atualizarFormulario);
    if (radioPix) radioPix.addEventListener('change', atualizarFormulario);
    if (radioBoleto) radioBoleto.addEventListener('change', atualizarFormulario);
    
    // Executa imediatamente ao abrir a página
    atualizarFormulario();
});