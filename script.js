let resultados = {}; 
let metodos = [];
let indiceMetodo = 0;
let indiceEstado = 0;
let caminhoAtual = [];

const proximoBtn = document.getElementById('proximo-btn');
proximoBtn.disabled = true;

document.getElementById('resolver-btn').addEventListener('click', enviarDados);
proximoBtn.addEventListener('click', proximoEstado);
document.getElementById('resetar-btn').addEventListener('click', resetar);

// Função para lidar com "Selecionar Todos"
document.getElementById('selecionar-todos').addEventListener('change', function () {
    const todos = this.checked;
    document.querySelectorAll('input[name="algoritmo"]').forEach(input => {
        if (input.id !== 'selecionar-todos') {
            input.checked = todos;
        }
    });
});

// Se clicar em qualquer outro checkbox, desmarca "Selecionar Todos"
document.querySelectorAll('input[name="algoritmo"]').forEach(input => {
    if (input.id !== 'selecionar-todos') {
        input.addEventListener('change', function () {
            if (!this.checked) {
                document.getElementById('selecionar-todos').checked = false;
            }
        });
    }
});

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

    mudarCorDeFundo(); // Voltar tudo para o normal
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
        
        mostrarEstado();
        proximoBtn.style.visibility = 'visible';
        proximoBtn.disabled = false;
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function mostrarEstado() {
    const metodo = metodos[indiceMetodo];
    const estado = caminhoAtual[indiceEstado];

    document.getElementById('nome-solucao').textContent = `Método: ${metodo.toUpperCase()}`;

    const saida = document.getElementById('saida');
    saida.innerHTML = estado.map(valor => `
        <div>${valor === 0 ? '' : valor}</div>
    `).join('');

    mudarCorDeFundo(metodo); // Mudar cores das laterais
}

function proximoEstado() {
    indiceEstado++;
    if (indiceEstado < caminhoAtual.length) {
        mostrarEstado();
        atualizarContador();
    } else {
        mostrarResultados();
    }
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

    indiceMetodo++;
    if (indiceMetodo < metodos.length) {
        indiceEstado = 0;
        caminhoAtual = resultados[metodos[indiceMetodo]].solucao;
        document.getElementById('movimentos-numero').textContent = '0';
        mostrarEstado();
    } else {
        proximoBtn.disabled = true;
        proximoBtn.style.visibility = 'hidden';
        mudarCorDeFundo(); // volta pro normal
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
