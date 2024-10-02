__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"


import random
from typing import List, Callable
from tqdm import tqdm
import numpy as np

from .Individual import Individual
from ..Position import Position
from ..MusicPiece import MusicPiece


def genetic_loop(music_piece:MusicPiece,
         genome_length:int,
         cost_function:Callable[[List[int], MusicPiece, List[Position]], float],
         num_generations:int=100,
         num_population:int=100,
         mutation_rate:float=0.1,
         crossover_rate:float=0.7,
         the_seed:int=4,
         K_best:int=100,
         genome_values:List[List[int]]=None,
         cost_function_kwargs:dict={},
         save:bool=False):
    """Genetic main loop function for the optimization of music pieces"""

    # Set the seed
    random.seed(the_seed)

    # Initialize the population
    population = [Individual([random.choice(genome_values[i]) for i in range(genome_length)],
                                mutation_rate=mutation_rate,
                                single_point_crossover_rate=crossover_rate) for _ in range(num_population)]

    best_individual = Individual(genes=[0]*genome_length, fitness=-np.inf)

    if save:
        fitnesses = np.zeros((num_generations, num_population))

    # Main loop
    pbar = tqdm(range(num_generations))
    for generation in pbar:
        # Compute the fitness of the population
        for individual in population:
            individual.compute_fitness(lambda x: cost_function(x, music_piece, **cost_function_kwargs))

        # Sort the population by fitness
        population.sort(key=lambda x: x.fitness, reverse=True)
        
        if save:
            fitnesses[generation] = [individual.fitness for individual in population]

        # Update the best individual
        if population[0].fitness > best_individual.fitness:
            best_individual = population[0].copy()
            pbar.set_description(f"Best fitness: {round(best_individual.fitness)}")
            
        # Crossover
        new_population = list[Individual]()

        while len(new_population) < num_population // 3:
            parent1 = random.choice(population[:K_best])
            parent2 = random.choice(population)
            child1, child2 = parent1.single_point_crossover(parent2)
            new_population.append(child1)
            new_population.append(child2)

        while len(new_population) < num_population:
            parent1 = random.choice(population[:K_best])
            parent2 = random.choice(population[:K_best])
            child1, child2 = parent1.double_point_crossover(parent2)
            new_population.append(child1)
            new_population.append(child2)

        # Mutate
        for individual in new_population:
            individual.mutate(genome_values)

        # Replace the population
        population = new_population
    
    if save:
        # write over the saved fitnesses (last generation)
        with open("src/genetic_optim/saved/fitnesses.npy", "wb") as f:
            np.save(f, fitnesses)
        
        # save the fitnesses for this run forever
        with open(f"src/genetic_optim/saved/fitnesses_{num_generations}_{num_population}_{the_seed}_{mutation_rate}_{crossover_rate}.npy", "wb") as f:
            np.save(f, fitnesses)


    # Return the best individual
    return best_individual