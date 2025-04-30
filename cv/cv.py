import numpy as np
import math
import random
import copy
import matplotlib.pyplot as plt

class AnnealingModel:
    def __init__(self, file, sa_max=500, cooling_scheme='exponential'):
        self.SA_MAX = sa_max
        self.file = file
        self.cooling_scheme = cooling_scheme
        self._MINIMUN_TEMPERATURE = 0.01
        self._BASE_COOLING_RATE = 0.95
        self.current_temperature = 1000
        self.energy_history = []
        self.temperature_history = []
        self.best_energy_overall = float('inf')
        self.best_state_overall = None

        self.table = self.load_coordenates()
        self.matrix = self.create_matrix_n_n()
        self.state = self.random_initial_state()
        self.determine_initial_temp()

    def determine_initial_temp(self, num_samples=100):
        energies = []
        current_energy = self.calculate_energy(self.state)
        for _ in range(num_samples):
            new_state = self.get_random_state(self.state)
            new_energy = self.calculate_energy(new_state)
            energies.append(abs(new_energy - current_energy))
        avg_delta = np.mean(energies)
        self.current_temperature = avg_delta * 10

    def random_initial_state(self):
        state = list(range(len(self.table)))
        random.shuffle(state)
        return state

    def accept_prob(self, delta):
        if delta < 0:
            return 1.0
        try:
            return math.exp(-delta / self.current_temperature)
        except OverflowError:
            return 0.0

    def pitagoras(self, pos1, pos2):
        x1, y1 = self.table[pos1][1], self.table[pos1][2]
        x2, y2 = self.table[pos2][1], self.table[pos2][2]
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    def get_random_state(self, state):
        new_state = copy.copy(state)
        num_swaps = random.randint(1, 5)
        for _ in range(num_swaps):
            i, j = random.sample(range(len(state)), 2)
            new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def calculate_energy(self, state):
        energy = 0
        for i in range(len(state)):
            energy += self.matrix[state[i]][state[(i + 1) % len(state)]]
        return energy

    def iteration_on_temp(self):
        current_state = copy.copy(self.state)
        current_energy = self.calculate_energy(current_state)

        for _ in range(self.SA_MAX):
            new_state = self.get_random_state(current_state)
            new_energy = self.calculate_energy(new_state)
            delta = new_energy - current_energy

            if delta < 0 or random.random() < self.accept_prob(delta):
                current_state = new_state
                current_energy = new_energy

                if current_energy < self.best_energy_overall:
                    self.best_energy_overall = current_energy
                    self.best_state_overall = copy.copy(current_state)

            self.energy_history.append(current_energy)
            self.temperature_history.append(self.current_temperature)

        return current_state

    def create_matrix_n_n(self):
        n = len(self.table)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i):
                dist = self.pitagoras(i, j)
                matrix[i][j] = dist
                matrix[j][i] = dist
        return matrix

    def load_coordenates(self):
        table = []
        with open(self.file, 'r') as f:
            for line in f:
                if line.strip() == "EOF":
                    break
                parts = line.strip().split()
                if len(parts) == 3:
                    try:
                        table.append([int(parts[0]), float(parts[1]), float(parts[2])])
                    except ValueError:
                        continue
        return table

    def cool_down(self, iteration):
        if self.cooling_scheme == 'exponential':
            self.current_temperature *= self._BASE_COOLING_RATE
        elif self.cooling_scheme == 'linear':
            self.current_temperature -= 1
        elif self.cooling_scheme == 'logarithmic':
            self.current_temperature = self.current_temperature / (1 + 0.001 * iteration)
        self.current_temperature = max(self.current_temperature, self._MINIMUN_TEMPERATURE)

    def run(self):
        iteration = 0
        while self.current_temperature > self._MINIMUN_TEMPERATURE:
            self.state = self.iteration_on_temp()
            self.cool_down(iteration)
            iteration += 1
        self.state = self.best_state_overall
        
        return self.best_energy_overall, self.energy_history