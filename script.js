// Variáveis globais
let resultados = {}; 
let metodos = [];
let indiceMetodo = 0;
let indiceEstado = 0;
let caminhoAtual = [];
let intervalo;
let animando = false;
let resultadosImpressos = false;

// Elementos
const proximoBtn = document.getElementById('proximo-btn');
const playPauseBtn = document.getElementById('play-pause-btn');
const restartBtn = document.getElementById('restart-btn');

proximoBtn.disabled = true;
playPauseBtn.disabled = true;
restartBtn.disabled = true;

// Event listeners

document.getElementById('resolver-btn').addEventListener('click', enviarDados);
proximoBtn.addEventListener('click', proximoMetodo);
playPauseBtn.addEventListener('click', toggleAnimacao);
restartBtn.addEventListener('click', restartAnimacao);
document.getElementById('resetar-btn').addEventListener('click', resetar);

document.getElementById('selecionar-todos').addEventListener('change', function () {
    const todos = this.checked;
    document.querySelectorAll('input[name="algoritmo"]').forEach(input => {
        if (input.id !== 'selecionar-todos') {
            input.checked = todos;
        }
    });
});

document.querySelectorAll('input[name="algoritmo"]').forEach(input => {
    if (input.id !== 'selecionar-todos') {
        input.addEventListener('change', function () {
            if (!this.checked) {
                document.getElementById('selecionar-todos').checked = false;
            }
        });
    }
});

// Funções principais

function resetar() {
    document.querySelectorAll('#tabuleiro-inicial input').forEach(input => {
        input.value = '';
    });
    document.querySelectorAll('input[name="algoritmo"]').forEach(input => {
        input.checked = false;
    });

    document.getElementById('saida').innerHTML = '';
    document.getElementById('resultados').innerHTML = '';
    document.getElementById('nome-solucao').textContent = '';
    document.getElementById('movimentos-numero').textContent = '0';

    proximoBtn.style.visibility = 'hidden';
    proximoBtn.disabled = true;
    playPauseBtn.disabled = true;
    restartBtn.disabled = true;

    clearInterval(intervalo);
    animando = false;

    mudarCorDeFundo();
}

function enviarDados() {
    document.getElementById('resultados').innerHTML = '';
    document.getElementById('movimentos-numero').textContent = '0';

    const tabuleiro = [];
    document.querySelectorAll('#tabuleiro-inicial input').forEach(input => {
        const valor = input.value.trim();
        tabuleiro.push(valor === '' ? 0 : parseInt(valor));
    });

    const algoritmos = [];
    document.querySelectorAll('input[name="algoritmo"]:checked').forEach(input => {
        algoritmos.push(input.value);
    });

    if (tabuleiro.length !== 9 || algoritmos.length === 0) {
        alert("Preencha corretamente o tabuleiro e selecione pelo menos um algoritmo!");
        return;
    }

    fetch('/resolver', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ tabuleiro, algoritmos })
    })
    .then(response => response.json())
    .then(data => {
        resultados = data;
        metodos = Object.keys(resultados);
        indiceMetodo = 0;
        indiceEstado = 0;
        caminhoAtual = resultados[metodos[indiceMetodo]].solucao;

        document.getElementById('saida').innerHTML = '';
        document.getElementById('nome-solucao').textContent = '';

        resultadosImpressos = false;

        mostrarEstado();

        proximoBtn.style.visibility = 'visible';
        proximoBtn.disabled = false;
        playPauseBtn.disabled = false;
        restartBtn.disabled = false;
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function mostrarEstado() {
    const metodo = metodos[indiceMetodo];
    const estado = caminhoAtual[indiceEstado];
    const saida = document.getElementById('saida');
    
    document.getElementById('nome-solucao').textContent = `Método: ${metodo.toUpperCase()}`;
    
    // Se for a primeira vez, criar os tiles
    if (!saida.hasChildNodes()) {
        estado.forEach((valor, i) => {
            if (valor === 0) return; // Não mostrar tile do vazio
            const div = document.createElement('div');
            div.className = 'tile';
            div.id = `tile-${valor}`;
            div.textContent = valor;
            saida.appendChild(div);
        });
    }

    estado.forEach((valor, i) => {
        const x = i % 3;
        const y = Math.floor(i / 3);
        if (valor === 0) return;

        const tile = document.getElementById(`tile-${valor}`);
        tile.style.left = `${x * 50}px`;
        tile.style.top = `${y * 50}px`;
    });

    mudarCorDeFundo(metodo);
}


function toggleAnimacao() {
    if (animando) {
        clearInterval(intervalo);
        animando = false;
        playPauseBtn.textContent = 'Play';
    } else {
        iniciarAnimacao();
        playPauseBtn.textContent = 'Pause';
    }
}

function iniciarAnimacao() {
    if (!animando) {
        animando = true;
        intervalo = setInterval(() => {
            indiceEstado++;
            if (indiceEstado < caminhoAtual.length) {
                mostrarEstado();
                atualizarContador();
            } else {
                clearInterval(intervalo);
                animando = false;
                playPauseBtn.textContent = 'Play';
                if (!resultadosImpressos) {
                    mostrarResultados();
                    resultadosImpressos = true;
                }
            }
        }, 500);
    }
}


function restartAnimacao() {
    clearInterval(intervalo);
    animando = false;
    indiceEstado = 0;
    document.getElementById('movimentos-numero').textContent = '0';
    mostrarEstado();
    playPauseBtn.textContent = 'Play';
}

function atualizarContador() {
    let movimentos = parseInt(document.getElementById('movimentos-numero').textContent);
    movimentos++;
    document.getElementById('movimentos-numero').textContent = movimentos;
}

function mostrarResultados() {
    const metodo = metodos[indiceMetodo];
    const dados = resultados[metodo];

    const resultadosDiv = document.getElementById('resultados');
    resultadosDiv.innerHTML += `
        <div class="movimento">
            <h3>Resultados para ${metodo.toUpperCase()}:</h3>
            <p>Nós gerados: ${dados.nos_gerados}</p>
            <p>Utilização de memória: ${dados.utilizacao_memoria}</p>
            <p>Profundidade da solução: ${dados.profundidade_solucao ?? 'Não encontrada'}</p>
            <p>Profundidade máxima: ${dados.profundidade_maxima}</p>
            <p>Admissibilidade: ${dados.admissibilidade ? 'Sim' : 'Não'}</p>
            <p>Ótima: ${dados.otima ? 'Sim' : 'Não'}</p>
            <p>Completa: ${dados.completa ? 'Sim' : 'Não'}</p>
        </div>
    `;

    if (!dados.profundidade_solucao) {
        mudarCorDeFundo('sem_solucao');
    }
}

function proximoMetodo() {
    indiceMetodo++;
    if (indiceMetodo < metodos.length) {
        indiceEstado = 0;
        caminhoAtual = resultados[metodos[indiceMetodo]].solucao;
        document.getElementById('movimentos-numero').textContent = '0';
        resultadosImpressos = false;
        mostrarEstado();
        playPauseBtn.disabled = false;
        restartBtn.disabled = false;
    } else {
        proximoBtn.disabled = true;
        playPauseBtn.disabled = true;
        restartBtn.disabled = true;
        mudarCorDeFundo()
    }
}

function mudarCorDeFundo(algoritmo) {
    const esquerda = document.getElementById('coluna-esquerda');
    const direita = document.getElementById('coluna-direita');
    const meio = document.getElementById('coluna-meio');

    // Deixar o meio sempre branco
    meio.style.backgroundColor = '#ffffff';

    switch (algoritmo) {
        case 'largura':
            esquerda.style.backgroundColor = '#add8e6'; // Azul claro
            direita.style.backgroundColor = '#add8e6';
            break;
        case 'profundidade':
            esquerda.style.backgroundColor = '#90ee90'; // Verde claro
            direita.style.backgroundColor = '#90ee90';
            break;
        case 'gulosa':
            esquerda.style.backgroundColor = '#ffffcc'; // Amarelo claro
            direita.style.backgroundColor = '#ffffcc';
            break;
        case 'aestrela':
            esquerda.style.backgroundColor = '#dda0dd'; // Roxo claro
            direita.style.backgroundColor = '#dda0dd';
            break;
        case 'sem_solucao':
            esquerda.style.backgroundColor = '#ffcccb'; // Vermelho claro
            direita.style.backgroundColor = '#ffcccb';
            break;
        default:
            esquerda.style.backgroundColor = '#f0f0f0'; // Cinzinha padrão
            direita.style.backgroundColor = '#f0f0f0';
    }
}
