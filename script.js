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
    resposta.textContent = resultado.mensagem;

    if (resultado.passos) {
    criarAnimacao(resultado.passos[0], resultado.passos); 
}

}

function criarAnimacao(tabuleiroInicial, passos) {
    const grid = document.getElementById('tabuleiro');
    grid.innerHTML = ''; // limpa a grade
    grid.style.position = 'relative';
    grid.style.width = '200px';
    grid.style.height = '200px';

    const blocos = {};

    for (let i = 0; i < 9; i++) {
        const valor = tabuleiroInicial[i];
        const bloco = document.createElement('div');
        bloco.className = 'tile';
        bloco.textContent = valor !== '0' ? valor : '';
        if (valor === '0') bloco.classList.add('zero');
        grid.appendChild(bloco);
        blocos[valor] = bloco;
        moverBloco(bloco, i);
    }

    let i = 0;
    function animarPasso() {
        if (i >= passos.length) return;
        const estado = passos[i];
        for (let j = 0; j < 9; j++) {
            const valor = estado[j];
            const bloco = blocos[valor];
            moverBloco(bloco, j);
        }
        i++;
        setTimeout(animarPasso, 500); // tempo entre passos
    }

    animarPasso();
}

function moverBloco(bloco, pos) {
    const x = pos % 3;
    const y = Math.floor(pos / 3);
    bloco.style.transform = `translate(${x * 70}px, ${y * 70}px)`;
}

