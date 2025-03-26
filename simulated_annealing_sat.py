import numpy as np

class AnnealingModel:
    def __init__(self, file):
        self.file = file
        self.expressions = []
        self.energy = 100
        self.temperature = 100
        self.setup()
    
    def setup(self):
        """
        Creates the environment based on the passed file
        """
        with open(self.file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                elements = line.split()
                if line.startswith('p'):
                    self.variables = np.random.choice([True, False], size=int(elements[-2]))
                    self.n_expressions = int(elements[-1])
                elif line.startswith('%'):
                    break
                elif not line.startswith('c'):
                    self.expressions.append([int(elements[0]), int(elements[1]), int(elements[2])])
                    
    def verify_result(self):
        """
        Verify how many expressions are true
        returns True, x if all expressions are true
        returns False, x if not all expressions are true
        x is how many expressions are true
        """
        positives = 0
        for expression in self.expressions:
            exp1 = self.variables[expression[0] - 1] if expression[0] > 0 else not self.variables[(expression[0] * -1) - 1]                 
            exp2 = self.variables[expression[1] - 1] if expression[1] > 0 else not self.variables[(expression[1] * -1) - 1]                 
            exp3 = self.variables[expression[2] - 1] if expression[2] > 0 else not self.variables[(expression[2] * -1) - 1]                 
            if exp1 and exp2 and exp3:
                positives += 1
        return positives == len(self.expressions), positives
                
    
        

if __name__ == "__main__":
    model = AnnealingModel(file='formulas/uf20-01.cnf')
    print(model.expressions[:10])
    print(model.n_expressions, len(model.variables))