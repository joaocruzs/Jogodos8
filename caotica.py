from collections import deque

objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def busca_em_largura(estado_inicial):
    # Certifique-se de que o estado inicial seja convertido para tupla
    estado_inicial = tuple(estado_inicial)
    
    fronteira = deque()
    fronteira.append((estado_inicial, [], 0))  # (estado, caminho, profundidade)
    visitados = set()
    nos_gerados = 1
    profundidade_max = 0
    maior_fronteira = 1

    while fronteira:
        maior_fronteira = max(maior_fronteira, len(fronteira))
        estado, caminho, profundidade = fronteira.popleft()
        visitados.add(estado)

        if estado == objetivo:
            return {
                "solucao": caminho,
                "nos_gerados": nos_gerados,
                "nos_fronteira": len(fronteira),
                "profundidade_solucao": profundidade,
                "profundidade_max": profundidade_max,
                "completo": True,
                "otimo": True,
                "admissivel": "Não se aplica (sem heurística)"
            }

        for sucessor in gerar_sucessores(estado):
            if sucessor not in visitados and not any(s[0] == sucessor for s in fronteira):
                fronteira.append((sucessor, caminho + [sucessor], profundidade + 1))
                nos_gerados += 1
                profundidade_max = max(profundidade_max, profundidade + 1)

    return {
        "solucao": None,
        "nos_gerados": nos_gerados,
        "nos_fronteira": len(fronteira),
        "profundidade_solucao": None,
        "profundidade_max": profundidade_max,
        "completo": False,
        "otimo": False,
        "admissivel": "Não se aplica (sem heurística)"
    }

objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)
LIMITE_PROFUNDIDADE = 30

def movimentos_possiveis(pos):
    return {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7]
    }[pos]

def gerar_sucessores(estado):
    pos_zero = estado.index(0)
    sucessores = []
    for mov in movimentos_possiveis(pos_zero):
        novo = list(estado)
        novo[pos_zero], novo[mov] = novo[mov], novo[pos_zero]
        sucessores.append(tuple(novo))  # Garantindo que o estado seja uma tupla
    return sucessores

def busca_em_profundidade(estado_inicial):
    pilha = [(estado_inicial, [], 0)]  # Pilha com o estado inicial, caminho e profundidade
    visitados = set()  # Set de visitados
    nos_gerados = 1
    profundidade_max = 0

    while pilha:
        estado, caminho, profundidade = pilha.pop()

        # Verifica se a profundidade ultrapassou o limite
        if profundidade > LIMITE_PROFUNDIDADE:
            continue

        visitados.add(tuple(estado))  # Aqui, garantimos que o estado seja uma tupla
        profundidade_max = max(profundidade_max, profundidade)

        if estado == objetivo:
            return {
                "solucao": caminho,
                "nos_gerados": nos_gerados,
                "nos_fronteira": len(pilha),
                "profundidade_solucao": profundidade,
                "profundidade_max": profundidade_max,
                "completo": False,  # DFS limitada não é completa
                "otimo": False,     # DFS não garante ótimos
                "admissivel": "Não se aplica (sem heurística)"
            }

        for s in gerar_sucessores(estado):
            if s not in visitados:
                pilha.append((s, caminho + [s], profundidade + 1))  # Aumenta a profundidade
                nos_gerados += 1

    return {
        "solucao": None,
        "nos_gerados": nos_gerados,
        "nos_fronteira": len(pilha),
        "profundidade_solucao": None,
        "profundidade_max": profundidade_max,
        "completo": False,
        "otimo": False,
        "admissivel": "Não se aplica (sem heurística)"
    }

import heapq

objetivo = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Movimentos possíveis
def movimentos_possiveis(pos):
    return {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7]
    }[pos]

# Função para calcular a distância de Manhattan de um estado para o objetivo
def heuristica(estado):
    distancia = 0
    for i, valor in enumerate(estado):
        if valor != 0:
            objetivo_pos = objetivo.index(valor)
            x1, y1 = i // 3, i % 3  # Posição no estado atual
            x2, y2 = objetivo_pos // 3, objetivo_pos % 3  # Posição no estado objetivo
            distancia += abs(x1 - x2) + abs(y1 - y2)  # Distância de Manhattan
    return distancia

# Função para gerar os sucessores de um estado
def gerar_sucessores(estado):
    pos_zero = estado.index(0)
    sucessores = []
    for mov in movimentos_possiveis(pos_zero):
        novo = list(estado)
        novo[pos_zero], novo[mov] = novo[mov], novo[pos_zero]
        sucessores.append(tuple(novo))  # Retorna o sucessor como tupla
    return sucessores

# Implementação do algoritmo A*
def a_estrela(estado_inicial):
    fronteira = []
    heapq.heappush(fronteira, (0 + heuristica(estado_inicial), 0, estado_inicial, []))  # (f(n), g(n), estado, caminho)
    visitados = set()
    nos_gerados = 1

    while fronteira:
        f, g, estado, caminho = heapq.heappop(fronteira)

        # Convertendo estado para tupla (imutável) para ser usado no conjunto
        estado = tuple(estado)

        if estado == objetivo:
            return {
                "solucao": caminho,
                "nos_gerados": nos_gerados,
                "nos_fronteira": len(fronteira),
                "profundidade_solucao": g,
                "profundidade_max": g,
                "completo": True,
                "otimo": True,
                "admissivel": "Sim"
            }

        if estado in visitados:
            continue
        visitados.add(estado)

        for sucessor in gerar_sucessores(estado):
            if sucessor not in visitados:
                g_novo = g + 1
                f_novo = g_novo + heuristica(sucessor)
                heapq.heappush(fronteira, (f_novo, g_novo, sucessor, caminho + [sucessor]))
                nos_gerados += 1

    return {
        "solucao": None,
        "nos_gerados": nos_gerados,
        "nos_fronteira": len(fronteira),
        "profundidade_solucao": None,
        "profundidade_max": g,
        "completo": False,
        "otimo": False,
        "admissivel": "Sim"
    }
