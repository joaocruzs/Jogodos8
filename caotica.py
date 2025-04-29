from collections import deque
import heapq

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
        sucessores.append(tuple(novo))
    return sucessores

def heuristica(estado):
    """ Heurística: número de peças fora do lugar """
    return sum(1 for i in range(9) if estado[i] != 0 and estado[i] != objetivo[i])

# Busca em Largura
def busca_em_largura(estado_inicial):
    estado_inicial = tuple(estado_inicial)
    fila = deque([(estado_inicial, [], 0)])
    visitados = set()
    nos_gerados = 1
    profundidade_maxima = 0

    while fila:
        estado, caminho, profundidade = fila.popleft()

        if profundidade > profundidade_maxima:
            profundidade_maxima = profundidade

        if estado == objetivo:
            return {
                "solucao": [list(estado_inicial)] + [list(e) for e in caminho],
                "utilizacao_memoria": len(fila),
                "nos_gerados": nos_gerados,
                "profundidade_solucao": profundidade,
                "profundidade_maxima": profundidade_maxima,
                "admissibilidade": True,
                # "otima": True,
                # "completa": True
            }

        visitados.add(estado)

        for s in gerar_sucessores(estado):
            if s not in visitados:
                fila.append((s, caminho + [s], profundidade + 1))
                nos_gerados += 1

    return {"solucao": [], "utilizacao_memoria": 0, "nos_gerados": nos_gerados, "profundidade_solucao": None,
            "profundidade_maxima": profundidade_maxima, "admissibilidade": True, "otima": False, "completa": False}

# Busca em Profundidade Limitada
def busca_em_profundidade(estado_inicial):
    estado_inicial = tuple(estado_inicial)
    pilha = [(estado_inicial, [], 0)]
    visitados = set()
    nos_gerados = 1
    profundidade_maxima = 0

    while pilha:
        estado, caminho, profundidade = pilha.pop()

        if profundidade > profundidade_maxima:
            profundidade_maxima = profundidade

        if profundidade > LIMITE_PROFUNDIDADE:
            continue

        if estado == objetivo:
            return {
                "solucao": [list(estado_inicial)] + [list(e) for e in caminho],
                "utilizacao_memoria": len(pilha),
                "nos_gerados": nos_gerados,
                "profundidade_solucao": profundidade,
                "profundidade_maxima": profundidade_maxima,
                "admissibilidade": False,
                "otima": False,
                "completa": False
            }

        visitados.add(estado)

        for s in gerar_sucessores(estado):
            if s not in visitados:
                pilha.append((s, caminho + [s], profundidade + 1))
                nos_gerados += 1

    return {"solucao": [], "utilizacao_memoria": 0, "nos_gerados": nos_gerados, "profundidade_solucao": None,
            "profundidade_maxima": profundidade_maxima, "admissibilidade": False, "otima": False, "completa": False}

# Busca Gulosa
def busca_gulosa(estado_inicial):
    estado_inicial = tuple(estado_inicial)
    fila = [(heuristica(estado_inicial), estado_inicial, [], 0)]
    visitados = set()
    nos_gerados = 1
    profundidade_maxima = 0

    while fila:
        _, estado, caminho, profundidade = heapq.heappop(fila)

        if profundidade > profundidade_maxima:
            profundidade_maxima = profundidade

        if estado == objetivo:
            return {
                "solucao": [list(estado_inicial)] + [list(e) for e in caminho],
                "utilizacao_memoria": len(fila),
                "nos_gerados": nos_gerados,
                "profundidade_solucao": profundidade,
                "profundidade_maxima": profundidade_maxima,
                "admissibilidade": False,
                "otima": False,
                "completa": False
            }

        visitados.add(estado)

        for s in gerar_sucessores(estado):
            if s not in visitados:
                heapq.heappush(fila, (heuristica(s), s, caminho + [s], profundidade + 1))
                nos_gerados += 1

    return {"solucao": [], "utilizacao_memoria": 0, "nos_gerados": nos_gerados, "profundidade_solucao": None,
            "profundidade_maxima": profundidade_maxima, "admissibilidade": False, "otima": False, "completa": False}

# Busca A*
def a_estrela(estado_inicial):
    estado_inicial = tuple(estado_inicial)
    fila = [(heuristica(estado_inicial), 0, estado_inicial, [], 0)]
    visitados = set()
    nos_gerados = 1
    profundidade_maxima = 0

    while fila:
        _, custo, estado, caminho, profundidade = heapq.heappop(fila)

        if profundidade > profundidade_maxima:
            profundidade_maxima = profundidade

        if estado == objetivo:
            return {
                "solucao": [list(estado_inicial)] + [list(e) for e in caminho],
                "utilizacao_memoria": len(fila),
                "nos_gerados": nos_gerados,
                "profundidade_solucao": profundidade,
                "profundidade_maxima": profundidade_maxima,
                "admissibilidade": True,
                "otima": True,
                "completa": True
            }

        if estado in visitados:
            continue

        visitados.add(estado)

        for s in gerar_sucessores(estado):
            if s not in visitados:
                novo_custo = custo + 1
                heapq.heappush(fila, (novo_custo + heuristica(s), novo_custo, s, caminho + [s], profundidade + 1))
                nos_gerados += 1

    return {"solucao": [], "utilizacao_memoria": 0, "nos_gerados": nos_gerados, "profundidade_solucao": None,
            "profundidade_maxima": profundidade_maxima, "admissibilidade": True, "otima": False, "completa": False}
