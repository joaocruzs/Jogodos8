// script.js

async function resolver() {
    const inputs = document.querySelectorAll('#tabuleiro input');
    const values = Array.from(inputs).map(input => input.value === '' ? '0' : input.value);

    // Verifica se todos os números de 0 a 8 estão presentes
    const numeros = new Set(values);
    const esperado = new Set(['0','1','2','3','4','5','6','7','8']);
    if (numeros.size !== 9 || ![...esperado].every(n => numeros.has(n))) {
        alert('Por favor, insira todos os números de 0 a 8 (sem repetir).');
        return;
    }

    const algoritmosSelecionados = Array.from(document.querySelectorAll('.algoritmos input:checked')).map(cb => cb.value);

    if (algoritmosSelecionados.length === 0) {
        alert('Por favor, selecione ao menos um método de resolução.');
        return;
    }

    const resposta = document.getElementById('resultado');
    resposta.textContent = 'Resolvendo...';

    try {
        const response = await fetch('/resolver', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tabuleiro: values,
                algoritmos: algoritmosSelecionados
            })
        });

        const resultado = await response.json();
        resposta.textContent = resultado.mensagem;
        // Aqui você pode chamar uma função para animar os passos

    } catch (error) {
        resposta.textContent = 'Erro ao resolver o jogo.';
        console.error(error);
    }
}
