__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List, Tuple, Callable
import numpy as np

class Individual:
    """Class representing an individual in a genetic algorithm"""

    def __init__(self, 
                 genes:List[int] = [], 
                 fitness:float = 0, 
                 mutation_rate:float = 0.01, 
                 crossover_rate:float = 0.7):
        self.genes = genes
        self.fitness = fitness
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    def __str__(self) -> str:
        return f"Individual with fitness {self.fitness} and genes {self.genes}"

    def __repr__(self) -> str:
        return f"Individual({self.genes}, {self.fitness}, {self.mutation_rate}, {self.crossover_rate})"

    def __eq__(self, other) -> bool:
        return self.genes == other.genes and self.fitness == other.fitness

    def mutate(self) -> None:
        """Mutates the individual"""
        for i in range(len(self.genes)):
            if np.random.rand() < self.mutation_rate:
                self.genes[i] = np.random.randint(0, 2)

    def crossover(self, other) -> Tuple["Individual", "Individual"]:
        """Crosses the individual with another one"""
        if np.random.rand() < self.crossover_rate:
            crossover_point = np.random.randint(0, len(self.genes))
            new_genes_1 = self.genes[:crossover_point] + other.genes[crossover_point:]
            new_genes_2 = other.genes[:crossover_point] + self.genes[crossover_point:]
            return Individual(new_genes_1), Individual(new_genes_2)
        return self, other

    def compute_fitness(self, cost_function:Callable[[List[int]], float]) -> None:
        """Computes the fitness of the individual"""
        self.fitness = cost_function(self.genes)