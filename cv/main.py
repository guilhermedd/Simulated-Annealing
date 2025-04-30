import matplotlib.pyplot as plt
from cv import AnnealingModel
import numpy as np

FILE = 100

def multiple_runs(file_path, cooling_schemes, sa_max=500):
    results = {}

    for scheme in cooling_schemes:
        all_energies = []
        all_histories = []
        for _ in range(10):
            model = AnnealingModel(file=file_path, sa_max=sa_max, cooling_scheme=scheme)
            best_energy, history = model.run()
            all_energies.append(best_energy)
            all_histories.append(history)
        
        results[scheme] = {
            'energies': all_energies,
            'avg': np.mean(all_energies),
            'std': np.std(all_energies),
            'histories': all_histories,
            'min': np.min(all_energies),
        }

    return results

def plot_boxplot(results):
    schemes = list(results.keys())
    data = [results[scheme]['energies'] for scheme in schemes]

    plt.figure(figsize=(10, 6))
    plt.boxplot(data, labels=schemes)
    plt.title("Boxplot de Energia Final por Esquema de Resfriamento")
    plt.ylabel("Energia Total")
    plt.xlabel("Esquema de Resfriamento")
    plt.grid(True)
    plt.savefig(f"boxplot_{FILE}.png")

def print_summary_table(results):
    print("Esquema\t\tMédia +/- Desvio\t\tMininmo")
    for scheme in results:
        avg = results[scheme]['avg']
        std = results[scheme]['std']
        min = results[scheme]['min']
        print(f"{scheme:<12}\t{avg:.2f} +/- {std:.2f}\t\t{min:.4f}")

def plot_convergence(results):
    for scheme, data in results.items():
        plt.figure(figsize=(8, 4))
        for i in range(10):
            plt.plot(data['histories'][i], alpha=0.5)
        plt.title(f"Convergência do SA - {scheme}")
        plt.xlabel("Iteração")
        plt.ylabel("Energia")
        plt.grid(True)
        plt.savefig(f"convergence_{FILE}.png")

if __name__ == "__main__":
    FILE_PATH = "../formulas/kroA100-tsp.txt"
    COOLING_SCHEMES = ['exponential', 'linear', 'logarithmic']

    results = multiple_runs(FILE_PATH, COOLING_SCHEMES)
    print_summary_table(results)
    plot_boxplot(results)
    plot_convergence(results)