import numpy as np
import math
import random
import copy
import matplotlib.pyplot as plt
from PIL import Image
import os

class AnnealingModel:
    def __init__(self, file):
        self.file = file
        self.energy = 100
        self.expressions = []
        self.current_temperature = 100_000
        self._COOLING_RATE = 0.99
        self._MINIMUN_TEMPERATURE = 0.1
        self._ITERATIONS_PER_TEMPERATURE = 200
        self.energy_history = []  # Lista para armazenar o histórico de energias
        self.setup()

    @property
    def is_done(self):
        return self.calculate_energy(self.state) == 0

    def accept_prob(self, delta):
        return math.exp(-delta / self.current_temperature)

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
        for _ in range(self._ITERATIONS_PER_TEMPERATURE):
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
            iteration += 1
            print(f"Iteração {iteration}: | Energia atual = {energy} | Temperatura atual = {self.current_temperature}")

        print(f"Treinamento concluído com energia final = {self.calculate_energy(self.state)}")
        self._generate_realtime_gif()

        return len(self.expressions) - self.calculate_energy(self.state)
    
    def _create_temp_dir(self):
        self.temp_dir = "temp_frames"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def _save_current_frame(self, iteration):
        """Salva o frame atual do gráfico"""
        plt.figure()
        plt.plot(range(len(self.energy_history)), self.energy_history, 'b-')
        plt.title(f'Evolução da Energia (Iteração {iteration})')
        plt.xlabel('Iteração')
        plt.ylabel('Energia')
        plt.grid(True)
        
        frame_path = os.path.join(self.temp_dir, f'frame_{iteration}.png')
        plt.savefig(frame_path, dpi=80)
        plt.close()
        self.frames.append(Image.open(frame_path))
        

    def _generate_realtime_gif(self):
        """Gera o GIF final a partir dos frames coletados"""
        gif_path = 'energy_evolution_realtime.gif'
        self.frames[0].save(
            gif_path,
            save_all=True,
            append_images=self.frames[1:],
            optimize=False,
            duration=100,
            loop=0
        )
        
        # Limpeza dos arquivos temporários
        for frame in self.frames:
            os.remove(frame.filename)
        os.rmdir(self.temp_dir)
        
        print(f'\nGIF gerado com sucesso: {gif_path}')


    def __str__(self):
        return f"Quantidade de expressões: {len(self.expressions)}\nQuantidade de variáveis: {len(self.state)}"
