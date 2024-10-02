__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from ..model.instrument.INeck import INeck

def getPosFromNotes(notes: List[str], instrument: INeck) -> int:
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (INeck): A neck instrument.

    Returns:
        int: The position to play the notes on the instrument.
    """
    
    posiblePositions = instrument.possible_positions(notes)

    if len(posiblePositions) == 0:
        return -1

    bestPosition = posiblePositions[0]

    for position in posiblePositions:
        if instrument.position_cost(position) < instrument.position_cost(bestPosition):
            bestPosition = position
    
    return bestPosition