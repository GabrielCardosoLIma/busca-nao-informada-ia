import time

class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices
        self.arestas = {v: [] for v in range(vertices)}

    def adicionar_aresta(self, u, v):
        self.arestas[u].append(v)
        self.arestas[v].append(u)  # Grafo não direcionado

    def busca_profundidade(self, inicio, objetivo, visitado=None):
        if visitado is None:
            visitado = set()
        
        visitado.add(inicio)
        
        if inicio == objetivo:
            return [inicio]
        
        for vizinho in self.arestas[inicio]:
            if vizinho not in visitado:
                caminho = self.busca_profundidade(vizinho, objetivo, visitado)
                if caminho:
                    return [inicio] + caminho
        
        return None

    def busca_profundidade_limitada(self, inicio, objetivo, limite, visitado=None):
        if visitado is None:
            visitado = set()
        
        return self._dls(inicio, objetivo, limite, visitado)

    def _dls(self, no, objetivo, limite, visitado):
        if limite < 0:
            return None
        
        visitado.add(no)
        
        if no == objetivo:
            return [no]
        
        for vizinho in self.arestas[no]:
            if vizinho not in visitado:
                caminho = self._dls(vizinho, objetivo, limite - 1, visitado)
                if caminho:
                    return [no] + caminho
        
        return None

    def medir_tempo_execucao(self, metodo_busca, *args):
        inicio_tempo = time.perf_counter_ns()
        resultado = metodo_busca(*args)
        fim_tempo = time.perf_counter_ns()
        return resultado, fim_tempo - inicio_tempo
    
# Exemplo de uso
grafo = Grafo(6)
grafo.adicionar_aresta(0, 1)
grafo.adicionar_aresta(0, 2)
grafo.adicionar_aresta(1, 3)
grafo.adicionar_aresta(2, 4)
grafo.adicionar_aresta(3, 5)
grafo.adicionar_aresta(4, 5)

inicio, objetivo = 0, 5

caminho_dfs, tempo_dfs = grafo.medir_tempo_execucao(grafo.busca_profundidade, inicio, objetivo)
caminho_dls, tempo_dls = grafo.medir_tempo_execucao(grafo.busca_profundidade_limitada, inicio, objetivo, 3)

print("Ponto inicial:", inicio)
print("Ponto final:", objetivo)
print("Caminho DFS:", caminho_dfs)
print("Tempo de execução DFS:", tempo_dfs)
print("Tamanho do caminho DFS:", len(caminho_dfs) if caminho_dfs else 0)
print("Caminho DLS (limite=3):", caminho_dls)
print("Tempo de execução DLS:", tempo_dls)
print("Tamanho do caminho DLS:", len(caminho_dls) if caminho_dls else 0)