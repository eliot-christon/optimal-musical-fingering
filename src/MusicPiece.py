__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from .instruments.Instrument import Instrument
from .midi.MidiTrack import MidiTrack
from .Position import Position

class MusicPiece:
    """Class representing a music piece"""

    def __init__(self, 
                 name:str = "music piece", 
                 description:str = "A music piece", 
                 instrument:Instrument = None,
                 track:MidiTrack = None):
        self.name       = name
        self.description= description
        self.instrument = instrument
        self.track      = track

    def __str__(self) -> str:
        return f"MusicPiece {self.name} [{self.instrument.name}]: {self.description} with {len(self.positions)} positions"
    
    def __repr__(self) -> str:
        return f"MusicPiece({self.name}, {self.description}, {self.instrument}, {self.track})"
        
    def compute_cost(self, positions:List[Position]) -> float:
        """Computes the cost of a list of positions"""
        cost = 0
        for i in range(len(positions)-1):
            cost += self.instrument.position_cost(positions[i])
            cost += self.instrument.transition_cost(positions[i], positions[i+1])
        return cost + self.instrument.position_cost(positions[-1])


if __name__ == "__main__":
    from .instruments.IKeyboard import IKeyboard
    from .midi.MidiObject import MidiObject
    from .functions_list_positions import get_basic_positions_from_midiroll

    piano = IKeyboard("piano")
    midi_file = MidiObject('src/midi/AUD_NK0155.mid')
    track = midi_file.better_tracks[4]

    print("Track {}: {}".format(4, track.name))
    
    positions = get_basic_positions_from_midiroll(track.get_first_roll())
    
    piece = MusicPiece("piece", "A piece of music", piano, track)
    
    print(piece.compute_cost(positions))