__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

import random
from typing import List
from tqdm import tqdm
import numpy as np

from ..MusicPiece import MusicPiece
from ..midi.MidiRoll import MidiRoll
from .utils import genome2positions, positions2genome
from .Individual import Individual

def cost_function(genome:List[int], music_piece:MusicPiece, base_positions:list = None) -> float:
    """Cost function for the genetic optimization"""
    if base_positions is None:
        base_positions = music_piece.positions
    return music_piece.compute_cost(genome2positions(genome, base_positions))


def main(music_piece:MusicPiece,
         num_generations:int=100,
         num_population:int=100,
         mutation_rate:float=0.1,
         crossover_rate:float=0.7,
         the_seed:int=4,
         K_best:int=100,
         save:bool=False):
    """Main function for the genetic optimization of fingering music pieces"""

    # Set the seed
    random.seed(the_seed)

    # Get the basic length of the genome
    base_positions = music_piece.positions
    genome_length = len(positions2genome(base_positions))
    genome_values = list(music_piece.instrument.fingers.keys())

    # Initialize the population
    population = [Individual([random.choice(genome_values) for _ in range(genome_length)],
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
            individual.compute_fitness(lambda x: cost_function(x, music_piece, base_positions))

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

if __name__ == "__main__":
    
    def scenario1():

        from ..instruments.IKeyboard import IKeyboard
        from ..midi.MidiObject import MidiObject
        from ..functions_list_positions import get_basic_positions_from_midiroll

        piano = IKeyboard("piano")
        midi_file = MidiObject('src/midi/AUD_NK0155.mid')
        track = midi_file.better_tracks[4]

        print("Track {}: {}".format(4, track.name))
        
        midi_roll = track.get_first_roll()
        clusters = midi_roll.divide_in_clusters(500)
        midi_roll = clusters[-1]
        
        base_positions = get_basic_positions_from_midiroll(midi_roll)
        piece = MusicPiece("piece", "A piece of music", piano, base_positions)

        best_individual = main(piece, 
                            the_seed=4, 
                            save=True, 
                            num_generations=100, 
                            num_population=1000,
                            mutation_rate=0.1,
                            crossover_rate=0.7,
                            K_best=80)
        print(best_individual)

        # print positions
        positions = genome2positions(best_individual.genes, get_basic_positions_from_midiroll(midi_roll))
        for i in range(len(positions)-1):
            pos = positions[i]
            next_pos = positions[i+1]
            print(pos, "cost:", piano.position_cost(pos, display=True), "transition cost:", piano.transition_cost(pos, next_pos, display=True))
        print(positions[-1], "cost:", piano.position_cost(positions[-1]))
        
        print("Total cost:", -best_individual.fitness)

        print(len(positions), "positions")
        
    def scenario2():
        from ..instruments.INeck import Guitar
        from ..Position import NPosition
        
        
        Fmaj7 = NPosition.from_strings_frets(fingers=[1, 3, 2, 4], strings=[6, 4, 3, 2], frets=[1, 3, 2, 3])
        Amaj7 = NPosition.from_strings_frets(fingers=[0, 1, 2, 3, 0], strings=[5, 4, 3, 2, 1], frets=[0, 2, 2, 2, 0])
        Dmin7 = NPosition.from_strings_frets(fingers=[0, 2, 3, 1], strings=[4, 3, 2, 1], frets=[0, 2, 3, 1])
        
        base_positions = [Fmaj7, Amaj7, Dmin7]
        
        instrument = Guitar()
        
        piece = MusicPiece("piece", "A piece of music", instrument, base_positions)
        
        best_individual = main(piece, 
                            the_seed=4, 
                            save=True, 
                            num_generations=100, 
                            num_population=1000,
                            mutation_rate=0.1,
                            crossover_rate=0.7,
                            K_best=80)
        
        # print positions
        positions = genome2positions(best_individual.genes, base_positions)
        for i in range(len(positions)-1):
            pos = positions[i]
            next_pos = positions[i+1]
            print(pos, "cost:", instrument.position_cost(pos, display=True), "transition cost:", instrument.transition_cost(pos, next_pos, display=True))
        print(positions[-1], "cost:", instrument.position_cost(positions[-1]))
        
        print("Total cost:", -best_individual.fitness)

        print(len(positions), "positions")
        
    
    
    
    # RUN SCENARIO
    scenario2()