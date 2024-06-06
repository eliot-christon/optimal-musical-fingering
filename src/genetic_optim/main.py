__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import random
from typing import List
from tqdm import tqdm
import numpy as np
import os

from ..functions_list_positions import get_basic_positions_from_midiroll
from ..MusicPiece import MusicPiece
from .utils import genome2positions, positions2genome
from .Individual import Individual

def fitness_function(genome:List[int], music_piece:MusicPiece, base_positions:list = None, reference_cost:float = 1000.) -> float:
    """Fitness function for the genetic optimization"""
    if base_positions is None:
        base_positions = get_basic_positions_from_midiroll(music_piece.track.get_first_roll())
    positions = genome2positions(genome, base_positions)
    return reference_cost - music_piece.compute_cost(positions)


def main(music_piece:MusicPiece,
         num_generations:int=100,
         num_population:int=100,
         mutation_rate:float=0.1,
         crossover_rate:float=0.7,
         the_seed:int=4,
         save:bool=False):
    """Main function for the genetic optimization of fingering music pieces"""

    # Set the seed
    random.seed(the_seed)

    # Get the basic length of the genome
    base_positions = get_basic_positions_from_midiroll(music_piece.track.get_first_roll())
    reference_cost = music_piece.compute_cost(base_positions)
    genome_length = len(positions2genome(base_positions))
    genome_values = list(music_piece.instrument.fingers.keys())

    # Initialize the population
    population = [Individual([random.choice(genome_values) for _ in range(genome_length)]) for _ in range(num_population)]

    if save:
        fitnesses = np.zeros((num_generations, num_population))

    # Main loop
    for generation in tqdm(range(num_generations)):
        # Compute the fitness of the population
        for individual in population:
            individual.compute_fitness(lambda x: fitness_function(x, music_piece, base_positions, reference_cost))

        # Sort the population by fitness
        population.sort(key=lambda x: x.fitness, reverse=True)
        
        if save:
            fitnesses[generation] = [individual.fitness for individual in population]

        # Crossover
        new_population = list[Individual]()
        for i in range(num_population//2):
            new_population += population[i].crossover(population[i+1])

        # Mutate
        for individual in new_population:
            individual.mutate()

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
    return population[0]


if __name__ == "__main__":

    from ..instruments.IKeyboard import IKeyboard
    from ..midi.MidiObject import MidiObject

    piano = IKeyboard("piano")
    midi_file = MidiObject('src/midi/AUD_NK0155.mid')
    track = midi_file.better_tracks[4]

    print("Track {}: {}".format(4, track.name))
    
    piece = MusicPiece("piece", "A piece of music", piano, track)
    
    best_individual = main(piece, num_generations=100, num_population=1000, the_seed=4, save=True)
    print(best_individual)