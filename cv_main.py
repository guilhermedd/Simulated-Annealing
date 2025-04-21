import matplotlib.pyplot as plt
from src.annealing_model import AnnealingModel
import numpy as np
import statistics
import random
import math
from itertools import chain

SA_Max = 100 #iterações para equilibrio termico
TF = 0.1 #temperatura minima final
alpha = 0.95 #taxa de decaimento
file = "formulas/eil51-tsp.txt"

class SA():
    def __init__(self):
        self.T = 100000
        self.iterT = 0
        self.nxy = cv_carregar_instancia(file)
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

# TODO  sepah que fazer no src
def cv_gerar_nova_solucao(solucoes, matriz):
    nova_solucao = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
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



if __name__ == "__main__":
    sa = SA()
    print(sa.run())
