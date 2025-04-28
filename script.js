async function resolver() {
    const inputs = document.querySelectorAll('#tabuleiro input');
    const values = Array.from(inputs).map(input => input.value === '' ? '0' : input.value);

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
        const respostaServidor = resultado.resposta;

        const metodo = Object.keys(respostaServidor)[0];
        const solucao = respostaServidor[metodo].solucao;

        if (solucao && solucao.length > 0) {
            animarSolucao(solucao);

            window.scrollTo({ top: 0, behavior: 'smooth' });

            resposta.innerHTML = `
                <b>Método:</b> ${metodo.toUpperCase()}<br>
                <b>Nós gerados:</b> ${respostaServidor[metodo].nos_gerados}<br>
                <b>Nós em fronteira:</b> ${respostaServidor[metodo].nos_fronteira}<br>
                <b>Profundidade da solução:</b> ${respostaServidor[metodo].profundidade_solucao}<br>
                <b>Profundidade máxima:</b> ${respostaServidor[metodo].profundidade_max}<br>
                <b>Completo:</b> ${respostaServidor[metodo].completo}<br>
                <b>Ótimo:</b> ${respostaServidor[metodo].otimo}<br>
                <b>Admissível:</b> ${respostaServidor[metodo].admissivel}<br>
            `;
        } else {
            resposta.textContent = 'Não foi encontrada solução.';
        }

    } catch (error) {
        resposta.textContent = 'Erro ao resolver o jogo.';
        console.error(error);
    }
}

function atualizarTabuleiro(estado) {
    const inputs = document.querySelectorAll('#tabuleiro input');
    for (let i = 0; i < estado.length; i++) {
        inputs[i].value = estado[i] === 0 ? '' : estado[i];
    }
}

function animarSolucao(solucoes) {
    let i = 0;
    const intervalo = setInterval(() => {
        if (i < solucoes.length) {
            const estadoAtual = Array.from(solucoes[i]);
            atualizarTabuleiro(estadoAtual);
            i++;
        } else {
            clearInterval(intervalo);
        }
    }, 800);
}
