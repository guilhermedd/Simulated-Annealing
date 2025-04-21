import matplotlib.pyplot as plt
from src.annealing_model import AnnealingModel
import numpy as np
import statistics
from itertools import chain




def cv_main():
    file = "formulas/eil51-tsp.txt"
    nxy = cv_carregar_instancia(file)
    matrix = cv_fazer_matriz_n_n(nxy)
    
    solucao_placeholder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
    distancia_total_placeholder = cv_calcular_distancia_total_da_solucao(solucao_placeholder, matrix)
    print(f"Distancia total da solucao: {distancia_total_placeholder}")

    cv_gerar_vizinho()
    return

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
    """faz matriz diagonal (NAO TA DIAGONAL MAS N FAZ MAL - faz sim...) de distancias entre os pontos"""
    last = len(nxy)
    matriz = [[0 for _ in range(last)] for _ in range(last)]
    i = 0
    j = 0

    for i in range(0, last):
        for j in range(0, last):
            distancia_entre_pontos = pitagoras(
                x1= nxy[i][1], y1= nxy[i][2], 
                x2= nxy[j][1], y2 = nxy[j][2]
            )
            matriz[i][j] = distancia_entre_pontos
    return matriz

# TODO  sepah que fazer no src
def cv_gerar_vizinho():
    return

def cv_calcular_distancia_total_da_solucao(solucao, matriz):
    distancia_total = 0
    for i in range(len(solucao) - 3):
        distancia_total += matriz[solucao[i]][solucao[i + 1]] + matriz[solucao[i + 1]][solucao[i + 2]]
    return distancia_total

def pitagoras(x1, y1, x2, y2) -> float: 
    """Calcula a distância entre dois pontos."""
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    pitagoras = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return pitagoras







# def run_experiment(file, sa_max=1):
#     """Executa uma simulação e retorna os históricos."""
#     model = AnnealingModel(file=file, sa_max=sa_max)
#     energy, temperature_history, energy_history = model.main()
#     return energy, temperature_history, energy_history

# def plot_best_runs(best_runs, file):
#     """Plota 3 subplots com os melhores resultados (menor energia) para cada SA_MAX."""
#     fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharex=True)

#     for i, (sa_max, energy_history, temperature_history) in enumerate(best_runs):
#         ax1 = axs[i]
#         ax1.set_title(f'SA_MAX = {sa_max}')
#         ax1.set_xlabel('Iterações')
#         ax1.set_ylabel('Energia', color='tab:blue')
#         ax1.plot(energy_history, 'b-', label='Energia')
#         ax1.tick_params(axis='y', labelcolor='tab:blue')

#         ax2 = ax1.twinx()
#         ax2.set_ylabel('Temperatura', color='tab:red')
#         ax2.plot(temperature_history, 'r-', label='Temperatura')
#         ax2.tick_params(axis='y', labelcolor='tab:red')

#     plt.tight_layout()
#     plt.savefig(f'melhores_sa_{file}.png')
#     plt.close()

# def plot_boxplot(data, file):
#     """Plota boxplot dos resultados finais (30 execuções por SA_MAX)."""
#     plt.figure(figsize=(8, 6))
#     plt.boxplot(data, vert=True, patch_artist=True, boxprops=dict(facecolor='lightblue'))
#     plt.title('Distribuição das Energias Finais (30 execuções)')
#     plt.xticks(ticks=[1, 2, 3], labels=[f'SA_MAX = {x}' for x in [1, 5, 10]])
#     plt.ylabel('Energia Final')
#     plt.grid(True, linestyle='--', alpha=0.6)
#     plt.savefig(f'boxplot_{file}.png')
#     plt.close()

if __name__ == "__main__":
    cv_main()
    # files = ["eil51-tsp.txt", "kroA100-tsp.txt"]
    # SA_MAXES = [1, 5, 10]
    # all_stats = {}  # file -> lista de 3 listas (uma por SA_MAX)

    # for file in files:
    #     best_runs = []
    #     stats_por_file = []

    #     for sa_max in SA_MAXES:
    #         resultados = []  # energia final
    #         energias = []    # lista dos vetores energia por iteração
    #         temperaturas = []  # lista dos vetores temperatura por iteração

            
    #         for i in range(30):
    #             energia_final, temperatura_hist, energia_hist = run_experiment(file=f"formulas/{file}", sa_max=sa_max)
    #             resultados.append(energia_final)
    #             energias.append(energia_hist)
    #             temperaturas.append(temperatura_hist)
                
    #         flat_energies = list(chain.from_iterable(energias))
    #         mean_energies = statistics.mean(flat_energies)
    #         std_energies = statistics.stdev(flat_energies)
    #         mean_results = statistics.mean(resultados)
    #         std_results = statistics.stdev(resultados)
    #         with open("resultados.txt", "a", encoding="utf-8") as f:
    #             f.write("\nEnergias\n")
    #             print("Energias")
    #             f.write(f"Arquivo: uf{file}-01.cnf, SA_MAX: {sa_max}, Média: {mean_energies:.2f}, Desvio: {std_energies:.2f}\n")
    #             print(f"Arquivo: uf{file}-01.cnf, SA_MAX: {sa_max}, Média: {mean_energies:.2f}, Desvio: {std_energies:.2f}")
    #             f.write("\nResultados\n")
    #             print("Resultados")
    #             f.write(f"Arquivo: uf{file}-01.cnf, SA_MAX: {sa_max}, Média: {mean_results:.2f}, Desvio: {std_results:.2f}\n")
    #             print(f"Arquivo: uf{file}-01.cnf, SA_MAX: {sa_max}, Média: {mean_results:.2f}, Desvio: {std_results:.2f}")

    #         # salvar resultados para a média e desvio
    #         stats_por_file.append(resultados)

    #         # escolher melhor execução (menor energia final)
    #         best_index = np.argmin(resultados)
    #         best_energy = energias[best_index]
    #         best_temp = temperaturas[best_index]
    #         best_runs.append((sa_max, best_energy, best_temp))

    #     all_stats[file] = stats_por_file

    #     # Plots
    #     plot_best_runs(best_runs, file)
    #     plot_boxplot(stats_por_file, file)

    # # Gerar tabela com médias e desvios
    # with open("tabela_medias_desvios.txt", "w") as f:
    #     f.write("Arquivo\tSA_MAX\tMédia Energia Final\tDesvio Padrão\n")
    #     f.write("=" * 50 + "\n")

    #     for file in files:
    #         f.write(f"uf{file}-01.cnf\n")
    #         sa_energias = all_stats[file]
    #         for idx, sa_max in enumerate(SA_MAXES):
    #             energias = sa_energias[idx]
    #             media = statistics.mean(energias)
    #             desvio = statistics.stdev(energias)
    #             f.write(f"\tSA={sa_max}\t{media:.2f}\t\t\t{desvio:.2f}\n")
    #         f.write("\n")


