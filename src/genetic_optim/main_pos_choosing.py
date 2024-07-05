__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

"""
This time, the genetic optimization will be done on the positions of the music piece.
Instead of creating the possible positions, we encode them in a genome and optimize this genome so that the cost function is minimized.
This method requires an already existing function for all plausible positions fingerings.
"""

from typing import List
import numpy as np

from ..Position import Position
from ..MusicPiece import MusicPiece
from ..instruments.Instrument import Instrument


def positions2genome(positions:List[Position], all_possible_positions:List[List[Position]]) -> List[int]:
    """Converts a list of positions to a genome"""
    assert len(positions) == len(all_possible_positions)
    # nb combinations in total is the product of the number of possible positions for each position
    nb_combinations = np.prod([len(all_possible_positions[i]) for i in range(len(positions))])
    # genome is a list of 0 and 1, the concatenation of the binary representation of the index of the combination. 2**len(g) > nb_combinations => len(g) > log2(nb_combinations)
    genome_length = int(np.ceil(np.log2(nb_combinations)))
    combination_number = 0
    for i in range(len(positions)):
        combination_number *= len(all_possible_positions[i])
        combination_number += all_possible_positions[i].index(positions[i])
    print(f"genome_length: {genome_length} => {2**genome_length} > {nb_combinations} combinations, combination_number: {combination_number}")
    return [int(i) for i in bin(combination_number)[2:].zfill(genome_length)]


def genome2positions(genome:List[int], all_possible_positions:List[List[Position]]) -> List[Position]:
    """Converts a genome to a list of positions"""
    # genome is a list of 0 and 1, the concatenation of the binary representation of the index of the combination. 2**len(g) > nb_combinations => len(g) > log2(nb_combinations)
    combination_number = int("".join([str(i) for i in genome]), 2)
    positions = []
    for i in range(len(all_possible_positions)):
        positions.append(all_possible_positions[i][combination_number % len(all_possible_positions[i])])
        combination_number //= len(all_possible_positions[i])
    return positions


def cost_function(genome:List[int], music_piece:MusicPiece, all_possible_positions:List[List[Position]] = None) -> float:
    """Cost function for the genetic optimization"""
    return music_piece.compute_cost(genome2positions(genome, all_possible_positions))





if __name__ == "__main__":

    from .genetic_loop import genetic_loop

    def scenario1():

        from ..instruments.INeck import Guitar
        from ..Position import NPosition
        from ..utils.note2num import note2num

        guitar = Guitar()
        

        Fmaj7 = ['F2', 'F3', 'A3', 'D4']
        Amaj7 = ['A2', 'E3', 'G#3', 'C#4', 'E4']
        Dmin7 = ['D3', 'F3', 'C4', 'E4']
        Cmaj = ['C3', 'E3', 'G3']

        base_notes = [
            Fmaj7,
            ['E4'],
            # ['D4'],
            # ['C4'],
            Amaj7,
            ['G#4'],
            ['F#4'],
            ['F4'],
            Dmin7,
            ['C4'],
            ['B3'],
            ['A3'],
            Cmaj]
        base_notes = [[note2num(note) for note in notes] for notes in base_notes]

        all_possible_positions = []
        for notes in base_notes:
            positions = [pos for pos in guitar.possible_positions(notes) if guitar.is_valid_position(pos)]
            all_possible_positions.append(positions)
        
        base_positions = [all_possible_positions[i][0] for i in range(len(all_possible_positions))]
        piece = MusicPiece("piece", "A piece of music", guitar, base_positions)

        best_individual = genetic_loop(piece,
                            genome_length=len(positions2genome(base_positions, all_possible_positions)),
                            cost_function=cost_function,
                            cost_function_kwargs={"all_possible_positions": all_possible_positions},
                            the_seed=4, 
                            save=True,
                            num_generations=100, 
                            num_population=1000,
                            mutation_rate=0.05,
                            crossover_rate=0.4,
                            genome_values= [0, 1],
                            K_best=80
                            )
        print(best_individual)

        # print positions
        positions = genome2positions(best_individual.genes, all_possible_positions)
        for i in range(len(positions)-1):
            pos = positions[i].sort_by_string()
            print(pos)
            
    scenario1()
