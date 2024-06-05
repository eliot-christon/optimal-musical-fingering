__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List
import numpy as np
import mido

from .Position import Position
from .Instrument import Instrument
from .midi.MidiRoll import MidiRoll
from .midi.MidiTrack import MidiTrack

def get_positions_from_midiroll(roll:MidiRoll) -> List[Position]:
    """Get the positions from a midi roll. the figers will be set naively from 0, the id will be set to the index of the position"""
    positions = np.array([], dtype=Position)
    last_pos = Position([], [], 0)
    for i in range(roll.notes.shape[1]):
        notes = np.where(roll.notes[:, i] != 0)[0]
        fingers = list(range(len(notes)))
        if len(notes) == 0 or (len(notes) == len(last_pos.notes) and all(notes == last_pos.notes)):
            continue
        positions = np.append(positions, Position(notes, fingers, i))
        last_pos = positions[-1]
    
    return positions

def positions_cost(positions:List[Position], instrument:Instrument) -> float:
    """Computes the cost of a list of positions"""
    cost = 0
    for i in range(len(positions)-1):
        cost += instrument.position_cost(positions[i])
        cost += instrument.transition_cost(positions[i], positions[i+1])
    return cost + instrument.position_cost(positions[-1])



if __name__ == "__main__":

    from .IKeyboard import IKeyboard

    piano = IKeyboard("piano")
    
    def roll_2(track_number=4):
        from .midi.MidiObject import MidiObject
        midi_file = MidiObject('src/midi/AUD_NK0155.mid')
        # pretty print messages
        dict_channels = midi_file.better_tracks[track_number].channels
        channel_number = list(dict_channels.keys())[0]
        channel_events = dict_channels[channel_number]
        return MidiRoll.from_channel_events(channel_events)

    roll = roll_2(4)
    
    positions = get_positions_from_midiroll(roll)

    for pos in positions:
        print(pos, "cost:", piano.position_cost(pos))
    
    print("Total cost:", positions_cost(positions, piano))
