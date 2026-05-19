document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('alerta-container');
    
    if (container) {
        const alertas = container.querySelectorAll('.alerta-card');
        
        alertas.forEach(alerta => {
            // Tempo ativo no ecrã antes de começar a sumir (6 segundos)
            const tempoExibicao = 6000; 
            
            setTimeout(() => {
                alerta.classList.add('alerta-sumir');
                // Espera o fim da animação do CSS (500ms) para remover do DOM
                setTimeout(() => {
                    alerta.remove();
                }, 500);
            }, tempoExibicao);
        });
    }
});