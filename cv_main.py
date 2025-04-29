import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np
import random
import math

SA_Max = 10_000  # Iterações para equilíbrio térmico
TF = 1e-15  # Temperatura mínima final
alpha = 0.99  # Taxa de decaimento
file_51 = "formulas/eil51-tsp.txt"

historico_solucoes = []
historico_temperaturas = []

class SA:
    def __init__(self):
        self.T = 300
        self.iterT = 0
        self.nxy = cv_carregar_instancia(file_51)
        self.matriz = cv_fazer_matriz_n_n(self.nxy)
        self.solucoes = [cv_gerar_nova_solucao([], self.matriz)]
        self.atual = cv_calcular_distancia_total_da_solucao(self.solucoes[-1], self.matriz)
        self.melhorSolucaoObtidaAteEntao = self.atual

    def iteration_on_temp(self):
        if not self.solucoes:
            best_state = cv_gerar_nova_solucao(self.solucoes, self.matriz)
        else:
            best_state = self.solucoes[-1]
        for _ in range(SA_Max):
            new_state = cv_gerar_nova_solucao(self.solucoes, self.matriz)
            if not self.solucoes:
                old_vizinho = new_state
            else:
                old_vizinho = self.solucoes[-1]
            print("Old vizinho", old_vizinho)
            vizinho = cv_calcular_distancia_total_da_solucao(old_vizinho, self.matriz)
            delta = vizinho - self.atual
            if delta < 0:
                best_state = new_state
            else:
                if random.random() < math.exp(-delta / self.T):
                    best_state = new_state
            historico_solucoes.append(self.atual)
            historico_temperaturas.append(self.T)
        return best_state

    def run(self):
        max_it_per_temp = 10_000
        it_per_temp = 0
        while self.T > TF and it_per_temp < max_it_per_temp:
            self.solucoes.append(self.iteration_on_temp)

            self.T *= alpha
            self.iterT = 0
            it_per_temp += 1

        return self.atual

def cv_carregar_instancia(file):
    nxy = []
    with open(file, 'r') as f:
        for line in f:
            if line.strip() == "EOF":
                break
            nxy.append(line.strip().split())
    return nxy

def cv_fazer_matriz_n_n(nxy):
    last = len(nxy)
    matriz = [[0] * last for _ in range(last)]
    for i in range(last):
        for j in range(i):
            distancia = pitagoras(nxy[i][1], nxy[i][2], nxy[j][1], nxy[j][2])
            matriz[i][j] = distancia
            matriz[j][i] = distancia
    return matriz

def cv_gerar_nova_solucao(solucoes, matriz):
    num_cidades = len(matriz)
    if not solucoes:
        nova_solucao = list(range(1, num_cidades + 1))
        random.shuffle(nova_solucao)
    else:
        nova_solucao = deepcopy(solucoes[-1])
        i, j = random.sample(range(num_cidades), 2)
        nova_solucao[i], nova_solucao[j] = nova_solucao[j], nova_solucao[i]
    # if nova_solucao not in solucoes:
    #     solucoes.append(nova_solucao)
    return nova_solucao

def cv_calcular_distancia_total_da_solucao(solucao, matriz):
    distancia_total = 0
    last = len(solucao)
    for k in range(last):
        i = solucao[k]
        j = solucao[(k + 1) % last]
        distancia_total += matriz[i - 1][j - 1]
    return distancia_total

def pitagoras(x1, y1, x2, y2):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def plotar_solucao(solucao, nxy):
    x, y = [], []
    for cidade in solucao:
        x.append(int(nxy[cidade - 1][1]))
        y.append(int(nxy[cidade - 1][2]))
    x.append(x[0])
    y.append(y[0])
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title("Solução do Simulated Annealing")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid()
    plt.show()

def plotar_convergencia(historico_solucoes, historico_temperaturas):
    iteracoes = list(range(len(historico_solucoes)))
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(iteracoes, historico_solucoes, 'b-', label="Solução (Distância)")
    ax1.set_xlabel("Iterações")
    ax1.set_ylabel("Solução (Distância)", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid()

    ax2 = ax1.twinx()
    ax2.plot(iteracoes, historico_temperaturas, 'r--', label="Temperatura")
    ax2.set_ylabel("Temperatura", color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    fig.suptitle("Convergência da Solução e Temperatura")
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    sa = SA()
    melhor_solucao = sa.run()
    print(f"Melhor solução encontrada: {melhor_solucao}")
    plotar_solucao(solucoes[-1], sa.nxy)
    plotar_convergencia(historico_solucoes, historico_temperaturas)
