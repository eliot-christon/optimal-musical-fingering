__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from ..Position import Position
from ..MusicPiece import MusicPiece


def genome2positions(genome:List[int], base_positions:List[Position]) -> List[Position]:
    """Converts a genome to a list of positions"""
    count = 0
    out_positions = base_positions.copy()
    for position in out_positions:
        position.fingers = genome[count:count+len(position.fingers)]
        count += len(position.fingers)
    return out_positions

def positions2genome(positions:List[Position]) -> List[int]:
    """Converts a list of positions to a genome"""
    genome = []
    for position in positions:
        genome += position.fingers
    return genome

def cost_function(genome:List[int], music_piece:MusicPiece, base_positions:list = None) -> float:
    """Cost function for the genetic optimization"""
    if base_positions is None:
        base_positions = music_piece.positions
    return music_piece.compute_cost(genome2positions(genome, base_positions))



if __name__ == "__main__":

    from .genetic_loop import genetic_loop
    
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

        best_individual = genetic_loop(piece,
                            genome_length=len(positions2genome(base_positions)),
                            cost_function=cost_function,
                            the_seed=4, 
                            save=True, 
                            num_generations=100, 
                            num_population=1000,
                            mutation_rate=0.1,
                            crossover_rate=0.7,
                            genome_values= list(piece.instrument.fingers.keys()),
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
    
    # RUN SCENARIO
    scenario1()