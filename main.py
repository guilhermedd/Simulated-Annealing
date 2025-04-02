import matplotlib.pyplot as plt
import multiprocessing
from src.annealing_model import AnnealingModel

def run_experiment(i, file, results, lock):
    """Exécute une simulation et enregistre le résultat en toute sécurité."""
    model = AnnealingModel(file=file, iteration=i)
    print(model)
    energy, n_iterations, final_temp = model.main()
    
    with lock:  
        print(f"Equações resolvidas ({i}): {energy}")
        results.append(energy)

def plot_boxplot(data):
    """Affiche un boxplot des résultats."""
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, vert=True, patch_artist=True, boxprops=dict(facecolor='lightblue'))
    plt.title('Distribuição das Equações Resolvidas')
    plt.ylabel('Equações Resolvidas')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(f'boxplot_{file}.png')

if __name__ == "__main__":
    file = 250
    manager = multiprocessing.Manager() 
    results = manager.list()  
    lock = multiprocessing.Lock() 

    processes = []
    num_processes = 6
    k = 0
    
    for i in range(int(1, (30/num_processes) + 1)):
        for j in range(num_processes):
            p = multiprocessing.Process(target=run_experiment, args=(f'formulas/uf{file}-01.cnf', k, results, lock))
            processes.append(p)
            p.start()
            k += 1

        for p in processes:
            p.join()
        

    plot_boxplot(file, results)
