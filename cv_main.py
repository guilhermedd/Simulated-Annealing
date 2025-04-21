import matplotlib.pyplot as plt
from src.annealing_model import AnnealingModel
import numpy as np
import random
import math
from itertools import chain

SA_Max = 100 #iterações para equilibrio termico
TF = 0.1 #temperatura minima final
alpha = 0.95 #taxa de decaimento
file_51 = "formulas/eil51-tsp.txt"
file_101 = "formulas/kroA100-tsp.txt"

historico_solucoes = []
historico_temperaturas = []

class SA():
    def __init__(self):
        self.T = 100000
        self.iterT = 0
        self.nxy = cv_carregar_instancia(file_51)
        self.matriz = cv_fazer_matriz_n_n(self.nxy)
        self.solucoes = []
        self.solucoes = cv_gerar_nova_solucao(self.solucoes, self.matriz)
        self.atual = cv_calcular_distancia_total_da_solucao(self.solucoes[-1], self.matriz)
        self.melhorSolucaoObtidaAteEntao = self.atual 

    def run(self):
        while (self.T>TF):
            while (self.iterT < SA_Max) :
                print(f"atual: {self.atual}\titerT: {self.iterT}")
                self.iterT += 1
                self.solucoes = cv_gerar_nova_solucao(self.solucoes, self.matriz)
                vizinho = cv_calcular_distancia_total_da_solucao(self.solucoes[-1], self.matriz)

                delta = vizinho - self.atual
                if(delta < 0):
                    self.atual = vizinho
                    if(vizinho<self.melhorSolucaoObtidaAteEntao): self.melhorSolucaoObtidaAteEntao = vizinho
                else:
                    x = random.random()
                    if(x < math.exp( -delta / self.T)):
                        self.atual = vizinho
                
                historico_solucoes.append(sa.atual)
                historico_temperaturas.append(sa.T)

            self.T *= alpha     
            self.iterT = 0
        return self.melhorSolucaoObtidaAteEntao  

def cv_carregar_instancia(file):
    """Carrega uma lista de pontos N no plano em, X e Y."""
    nxy = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line == "EOF\n":
                break
            nxy.append(line.split())
    return nxy

def cv_fazer_matriz_n_n(nxy):
    """faz matriz diagonal (.) de distancias entre os pontos"""
    last = len(nxy)
    matriz = [[0] * last for _ in range(last)]

    for i in range(last):
        for j in range(i):
            distancia = pitagoras(
                x1= nxy[i][1], y1= nxy[i][2], 
                x2= nxy[j][1], y2 = nxy[j][2]
            )
            matriz[i][j] = distancia
            matriz[j][i] = distancia
    return matriz

def cv_gerar_nova_solucao(solucoes, matriz):
    num_cidades = len(matriz[0])
    nova_solucao = list(range(1, num_cidades + 1))

    random.shuffle(nova_solucao)
    if nova_solucao not in solucoes:
        solucoes.append(nova_solucao)
    return solucoes

def cv_calcular_distancia_total_da_solucao(solucao, matriz):
    distancia_total = 0
    last = len(solucao)
    for k in range(last):
        i = solucao[k]
        j = solucao[(k + 1) % last]  
        distancia_total += matriz[i-1][j-1]
    return distancia_total

def pitagoras(x1, y1, x2, y2) -> float: 
    """Calcula a distância entre dois pontos."""
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    pitagoras = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return pitagoras






def plotar_solucao(solucao, nxy):
    """Plota o gráfico da solução gerada."""
    x = []
    y = []
    for cidade in solucao:
        x.append(int(nxy[cidade - 1][1]))
        y.append(int(nxy[cidade - 1][2]))
    # Fechar o ciclo voltando ao ponto inicial
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
    """Plota a convergência da solução e a temperatura ao longo das iterações."""
    iteracoes = list(range(len(historico_solucoes)))

    fig, ax1 = plt.subplots(figsize=(8, 6))

    # Eixo primário: Solução
    ax1.plot(iteracoes, historico_solucoes, 'b-', label="Solução (Distância)")
    ax1.set_xlabel("Iterações")
    ax1.set_ylabel("Solução (Distância)", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid()

    # Eixo secundário: Temperatura
    ax2 = ax1.twinx()
    ax2.plot(iteracoes, historico_temperaturas, 'r--', label="Temperatura")
    ax2.set_ylabel("Temperatura", color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Título e legenda
    fig.suptitle("Convergência da Solução e Temperatura")
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    sa = SA()
    melhor_solucao = sa.run()
    print(f"Melhor solução encontrada: {melhor_solucao}")
    plotar_solucao(sa.solucoes[-1], sa.nxy)
    plotar_convergencia(historico_solucoes, historico_temperaturas)