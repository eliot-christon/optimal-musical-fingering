__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from ..model.instrument.INeck import INeck
from ..model.Position import NPosition

def getPosFromNotes(notes: List[str], instrument: INeck) -> NPosition:
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (INeck): A neck instrument.

    Returns:
        NPosition: The position to play the notes on the instrument.
    """
    
    posiblePositions = instrument.possible_positions(notes)
    posiblePositions = [pos for pos in posiblePositions if instrument.is_valid_position(pos)]

    if len(posiblePositions) == 0:
        return -1

    bestPosition = posiblePositions[0]

    for position in posiblePositions:
        if instrument.position_cost(position) < instrument.position_cost(bestPosition):
            bestPosition = position
    
    return bestPosition



if __name__ == "__main__":

    from ..model.instrument.INeck import Guitar
    from ..model.utils.note2num import note2num

    instrument = Guitar()
    notesInt = [note2num(note) for note in ['A2', 'F#3', 'C4', 'E4']]

    print(getPosFromNotes(notesInt, instrument))