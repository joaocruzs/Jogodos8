from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from algoritmos import busca_em_largura, busca_em_profundidade, busca_gulosa, a_estrela

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    data = request.get_json()

    if not data or 'tabuleiro' not in data or 'algoritmos' not in data:
        return jsonify({'error': 'Dados inválidos: esperado "tabuleiro" e "algoritmos"'}), 400

    tabuleiro = list(map(int, data['tabuleiro']))
    algoritmos = data['algoritmos']
    resposta = {}

    for alg in algoritmos:
        if alg == 'largura':
            resultado = busca_em_largura(tabuleiro)
        elif alg == 'profundidade':
            resultado = busca_em_profundidade(tabuleiro)
        elif alg == 'gulosa':
            resultado = busca_gulosa(tabuleiro)
        elif alg == 'aestrela':
            resultado = a_estrela(tabuleiro)
        else:
            resultado = {
                'utilizacao_memoria': 0,
                'nos_gerados': 0,
                'profundidade_solucao': None,
                'profundidade_maxima': 0,
                'admissibilidade': False,
                'caminho': []
            }
        resposta[alg] = resultado

    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)
