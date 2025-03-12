import time
import random
from collections import deque

def gerar_grafo(quantidade_vertices: int, arestas_por_vertice: int) -> dict:
    # Cria um grafo não direcionado com número fixo de arestas por vértice.
    grafo = {v: set() for v in range(quantidade_vertices)}
    
    for vertice in grafo:
        while len(grafo[vertice]) < arestas_por_vertice:
            vizinho = random.randint(0, quantidade_vertices - 1)
            if vizinho != vertice:
                grafo[vertice].add(vizinho)
                grafo[vizinho].add(vertice)  # Conexão bidirecional
    
    return grafo

def gerar_grafo_kn(quantidade_vertices: int, arestas_por_vertice: int) -> dict:
    # Gera um grafo kn onde cada vértice está conectado a exatamente k outros vértices de determinada.
    grafo = {v: set() for v in range(quantidade_vertices)}
    
    for vertice in range(quantidade_vertices):
        for i in range(1, arestas_por_vertice + 1):
            vizinho = (vertice + i) % quantidade_vertices
            grafo[vertice].add(vizinho)
            grafo[vizinho].add(vertice)
    
    return grafo

def busca_profundidade_iterativa(grafo: dict, inicio: int, objetivo: int) -> list:
    # Busca em profundidade (DFS) sem recursão para evitar estouro de pilha.
    # Sem recursão para evitar estouro de pilha.
    # Pré-ordem.
    pilha = [(inicio, [inicio])]
    visitados = set()
    
    while pilha:
        vertice, caminho = pilha.pop()
        if vertice == objetivo:
            return caminho
        
        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho in grafo[vertice]:
                pilha.append((vizinho, caminho + [vizinho]))
    
    return []

def busca_profundidade_limitada(grafo: dict, inicio: int, objetivo: int, limite: int) -> list:
    # Busca em profundidade com limite de profundidade (DLS).
    # Com limite de profundidade para caso atingir o limite a busca para no limite colocado.
    # Pré-ordem.
    pilha = [(inicio, [inicio], 0)]
    
    while pilha:
        vertice, caminho, profundidade = pilha.pop()
        if vertice == objetivo:
            return caminho
        
        if profundidade < limite:
            for vizinho in grafo[vertice]:
                pilha.append((vizinho, caminho + [vizinho], profundidade + 1))
    
    return []

def busca_largura(grafo: dict, inicio: int, objetivo: int) -> list:
    # Busca em largura (BFS)
    # Garante o menor caminho.
    fila = deque([(inicio, [inicio])])
    visitados = set()
    
    while fila:
        vertice, caminho = fila.popleft() # Remove da fila (FIFO)
        if vertice == objetivo:
            return caminho
        
        if vertice not in visitados:
            visitados.add(vertice)
            for vizinho in grafo[vertice]:
                fila.append((vizinho, caminho + [vizinho]))
    
    return []

def medir_tempo_execucao(funcao, *args) -> tuple:
    # Mede o tempo de execução de uma função.
    inicio_tempo = time.time()
    resultado = funcao(*args)
    tempo_execucao = (time.time() - inicio_tempo) * 1000  # Em milissegundos
    return resultado, tempo_execucao

def salvar_resultados(resultados, nome_arquivo="resultados_busca.csv"):
    # Gera um CSV pra ver os resultados.
    import csv
    
    campos = ['vertices', 'arestas', 'inicio', 'objetivo', 
              'dfs_tempo', 'dfs_caminho_tamanho', 
              'dls_tempo', 'dls_caminho_tamanho', 
              'bfs_tempo', 'bfs_caminho_tamanho']
    
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados)
    
    print(f"Resultados salvos em {nome_arquivo}")

def executar_testes():
    # Executa testes para medir desempenho das buscas.
    casos_teste = [
        (500, 3),
        (500, 5),
        (500, 7),
        (5000, 3),
        (5000, 5),
        (5000, 7),
        (10000, 3),
        (10000, 5),
        (10000, 7)
    ]
    
    resultados = []
    
    for vertices, arestas in casos_teste:
        print(f"\nTestando grafo com {vertices} vértices e {arestas} arestas por vértice")
        grafo = gerar_grafo(vertices, arestas)
        inicio, objetivo = 0, vertices - 1
        
        print(f"Ponto inicial: {inicio}, Ponto final: {objetivo}")
        
        caminho_dfs, tempo_dfs = medir_tempo_execucao(busca_profundidade_iterativa, grafo, inicio, objetivo)
        print(f"DFS: Tempo = {tempo_dfs:.4f}ms, Tamanho do Caminho = {len(caminho_dfs) if caminho_dfs else 'N/A'}")
        
        caminho_dls, tempo_dls = medir_tempo_execucao(busca_profundidade_limitada, grafo, inicio, objetivo, 20)
        print(f"DLS: Tempo = {tempo_dls:.4f}ms, Tamanho do Caminho = {len(caminho_dls) if caminho_dls else 'N/A'}")
        
        caminho_bfs, tempo_bfs = medir_tempo_execucao(busca_largura, grafo, inicio, objetivo)
        print(f"BFS: Tempo = {tempo_bfs:.4f}ms, Tamanho do Caminho = {len(caminho_bfs) if caminho_bfs else 'N/A'}")
        
        # Salva resultados p análise
        resultados.append({
            'vertices': vertices,
            'arestas': arestas,
            'inicio': inicio,
            'objetivo': objetivo,
            'dfs_tempo': tempo_dfs,
            'dfs_caminho_tamanho': len(caminho_dfs) if caminho_dfs else 'N/A',
            'dls_tempo': tempo_dls,
            'dls_caminho_tamanho': len(caminho_dls) if caminho_dls else 'N/A',
            'bfs_tempo': tempo_bfs,
            'bfs_caminho_tamanho': len(caminho_bfs) if caminho_bfs else 'N/A'
        })
        
        # Para mostrar caminhos (Decidimos comentar pois estava ficando muito grande)
        # print(f"Caminho DFS: {caminho_dfs}")
        # print(f"Caminho DLS: {caminho_dls}")
        # print(f"Caminho BFS: {caminho_bfs}")
    
    # Adicionar teste específico para o grafo kn
    print("\n\nTestando grafo kn com 10000 vértices e 7 arestas por vértice")
    grafo_kn = gerar_grafo_kn(10000, 7)
    inicio, objetivo = 0, 9999
    
    print(f"Ponto inicial: {inicio}, Ponto final: {objetivo}")
    
    caminho_dfs_kn, tempo_dfs_kn = medir_tempo_execucao(busca_profundidade_iterativa, grafo_kn, inicio, objetivo)
    print(f"DFS (grafo kn): Tempo = {tempo_dfs_kn:.4f}ms, Tamanho do Caminho = {len(caminho_dfs_kn) if caminho_dfs_kn else 'N/A'}")
    
    caminho_dls_kn, tempo_dls_kn = medir_tempo_execucao(busca_profundidade_limitada, grafo_kn, inicio, objetivo, 20)
    print(f"DLS (grafo kn): Tempo = {tempo_dls_kn:.4f}ms, Tamanho do Caminho = {len(caminho_dls_kn) if caminho_dls_kn else 'N/A'}")
    
    caminho_bfs_kn, tempo_bfs_kn = medir_tempo_execucao(busca_largura, grafo_kn, inicio, objetivo)
    print(f"BFS (grafo kn): Tempo = {tempo_bfs_kn:.4f}ms, Tamanho do Caminho = {len(caminho_bfs_kn) if caminho_bfs_kn else 'N/A'}")
    
    # Adiciona resultados grafo kn aos resultados geral
    resultados.append({
        'vertices': 10000,
        'arestas': 7,
        'inicio': inicio,
        'objetivo': objetivo,
        'dfs_tempo': tempo_dfs_kn,
        'dfs_caminho_tamanho': len(caminho_dfs_kn) if caminho_dfs_kn else 'N/A',
        'dls_tempo': tempo_dls_kn,
        'dls_caminho_tamanho': len(caminho_dls_kn) if caminho_dls_kn else 'N/A',
        'bfs_tempo': tempo_bfs_kn,
        'bfs_caminho_tamanho': len(caminho_bfs_kn) if caminho_bfs_kn else 'N/A'
    })
    
    # Salvar todos os resultados para visualização e analise
    salvar_resultados(resultados)

if __name__ == "__main__":
    executar_testes()