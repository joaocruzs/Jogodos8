# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from caotica import busca_em_largura, busca_em_profundidade, a_estrela

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    data = request.get_json()
    tabuleiro = list(map(int, data['tabuleiro']))
    algoritmos = data['algoritmos']
    resposta = {}

    for alg in algoritmos:
        if alg == 'largura':
            resultado = busca_em_largura(tabuleiro)
            resposta['largura'] = resultado
        elif alg == 'profundidade':
            resultado = busca_em_profundidade(tabuleiro)
            resposta['profundidade'] = resultado
        elif alg == 'a_estrela':
            resultado = a_estrela(tabuleiro)
            resposta['A*'] = resultado

    return jsonify({
        'resposta': resposta  
    })


def formatar_resultado(resposta):
    linhas = []
    for metodo, dados in resposta.items():
        linhas.append(f"\n=== Método: {metodo.upper()} ===")
        
        if 'solucao' in dados:
            linhas.append(f"Solução: {dados['solucao']}")
        
        for chave, valor in dados.items():
            if chave != 'solucao':
                linhas.append(f"{chave}: {valor}")
    
    return "\n".join(linhas)


if __name__ == '__main__':
    app.run(debug=True)