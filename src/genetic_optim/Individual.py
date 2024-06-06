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
        self.__genes = genes
        self.__fitness = fitness
        self.__mutation_rate = mutation_rate
        self.__crossover_rate = crossover_rate

    def __str__(self) -> str:
        return f"Individual with fitness {self.__fitness} and genes {self.__genes}"

    def __repr__(self) -> str:
        return f"Individual({self.__genes}, {self.__fitness}, {self.__mutation_rate}, {self.__crossover_rate})"

    def __eq__(self, other) -> bool:
        return self.__genes == other.genes and self.__fitness == other.fitness
    
    @property
    def genes(self) -> List[int]:
        return self.__genes
    
    @property
    def fitness(self) -> float:
        return self.__fitness
    
    def set_genes(self, genes:List[int]) -> None:
        self.__genes = genes

    def set_fitness(self, fitness:float) -> None:
        self.__fitness = fitness
    
    def mutate(self, values:List[int]) -> None:
        """Mutates the individual"""
        for i in range(len(self.__genes)):
            if np.random.rand() < self.__mutation_rate:
                self.__genes[i] = np.random.choice(values)

    def single_crossover(self, other) -> Tuple["Individual", "Individual"]:
        """Crosses the individual with another one"""
        if np.random.rand() < self.__crossover_rate:
            crossover_point = np.random.randint(0, len(self.__genes))
            new_genes_1 = self.__genes[:crossover_point] + other.genes[crossover_point:]
            new_genes_2 = other.genes[:crossover_point] + self.__genes[crossover_point:]
            return Individual(new_genes_1, mutation_rate=self.__mutation_rate, crossover_rate=self.__crossover_rate), \
                   Individual(new_genes_2, mutation_rate=self.__mutation_rate, crossover_rate=self.__crossover_rate)
        return self, other

    def compute_fitness(self, cost_function:Callable[[List[int]], float]) -> None:
        """Computes the fitness of the individual"""
        self.__fitness = -cost_function(self.__genes)
    
    def copy(self) -> "Individual":
        """Returns a copy of the individual"""
        return Individual(self.__genes.copy(), self.__fitness, self.__mutation_rate, self.__crossover_rate)