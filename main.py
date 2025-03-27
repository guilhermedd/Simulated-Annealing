from src.annealing_model import AnnealingModel

if __name__ == "__main__":
    model = AnnealingModel(file='formulas/uf250-01.cnf')
    print(model)
    solved = model.main()
    
    print(f"Equacoes resolvidas: {solved}")
