import numpy as np
import math
import random
import copy
import matplotlib.pyplot as plt

class AnnealingModel:
    def __init__(self, file, sa_max):
        self.file = file
        self.expressions = []
        self.current_temperature = 1000
        self._COOLING_RATE = 0.99
        self._MINIMUN_TEMPERATURE = 0.1
        self.SA_MAX = sa_max
        self.energy_history = []
        self.temperature_history = []
        self.setup()

    @property
    def is_done(self):
        return self.calculate_energy(self.state) == 0

    def accept_prob(self, delta):
        return 1 / (1 + math.exp(delta / self.current_temperature))


    def get_random_state(self, state):
        new_state = copy.copy(state)
        index = random.randint(0, len(state) - 1)
        new_state[index] = not new_state[index]
        return new_state

    def setup(self):
        """
        Cria o ambiente com base no arquivo fornecido.
        """
        with open(self.file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                elements = line.split()
                if line.startswith('p'):
                    self.state = np.random.choice([True, False], size=int(elements[-2]))
                    self.n_expressions = int(elements[-1])
                elif line.startswith('%'):
                    break
                elif not line.startswith('c'):
                    self.expressions.append([int(elements[0]), int(elements[1]), int(elements[2])])

    def calculate_energy(self, state):
        """
        Quanto menor a energia, melhor!
        Energia mínima = 0
        """
        energy = 0
        for expression in self.expressions:
            var1 = state[expression[0] - 1] if expression[0] > 0 else not state[abs(expression[0]) - 1]
            var2 = state[expression[1] - 1] if expression[1] > 0 else not state[abs(expression[1]) - 1]
            var3 = state[expression[2] - 1] if expression[2] > 0 else not state[abs(expression[2]) - 1]
            if not (var1 or var2 or var3):
                energy += 1  # Incrementa a energia quando a expressão não é satisfeita
        return energy

    def calculate_delta(self, old_state, new_state):
        return self.calculate_energy(new_state) - self.calculate_energy(old_state)

    def iteration_on_temp(self):
        best_state = copy.copy(self.state)
        for _ in range(self.SA_MAX):
            new_state = self.get_random_state(best_state)
            delta = self.calculate_delta(best_state, new_state)
            if delta < 0:
                best_state = new_state
            else:
                if random.random() < self.accept_prob(delta):
                    best_state = new_state
        return best_state

    def main(self):
        iteration = 0
        while self.current_temperature >= self._MINIMUN_TEMPERATURE and not self.is_done:
            self.state = self.iteration_on_temp()
            self.current_temperature *= self._COOLING_RATE
            energy = self.calculate_energy(self.state)
            
            self.energy_history.append(energy)
            self.temperature_history.append(self.current_temperature)
            
            iteration += 1
        
        return self.calculate_energy(self.state), self.temperature_history, self.energy_history
    
    def __str__(self):
        return f"Quantidade de expressões: {len(self.expressions)}\nQuantidade de variáveis: {len(self.state)}"