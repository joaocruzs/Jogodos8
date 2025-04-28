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
    // Limpar o tabuleiro inicial
    document.querySelectorAll('#tabuleiro-inicial input').forEach(input => {
        input.value = '';
    });

    // Desmarcar todos os algoritmos selecionados
    document.querySelectorAll('input[name="algoritmo"]').forEach(input => {
        input.checked = false;
    });

    // Limpar área de saída e resultados
    document.getElementById('saida').innerHTML = '';
    document.getElementById('resultados').innerHTML = '';
    document.getElementById('nome-solucao').textContent = '';

    // Zerar contador de movimentos
    document.getElementById('movimentos-numero').textContent = '0';

    // Esconder botão de próximo
    proximoBtn.style.visibility = 'hidden';
    proximoBtn.disabled = true;
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

    indiceMetodo++;
    if (indiceMetodo < metodos.length) {
        indiceEstado = 0;
        caminhoAtual = resultados[metodos[indiceMetodo]].solucao;
        document.getElementById('movimentos-numero').textContent = '0'; // Zera para novo método
        mostrarEstado();
    } else {
        proximoBtn.disabled = true;
        proximoBtn.style.visibility = 'hidden';
    }
}
