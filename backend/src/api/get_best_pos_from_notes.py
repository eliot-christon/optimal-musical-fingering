"""
This module contains the logic for determining the optimal finger positions
for a given set of musical notes and a specific instrument.
"""

from src.instruments.neck_instrument import NeckInstrument
from src.positions.neck_position import NeckPosition


def get_best_pos_from_notes(
    notes: list[int], input_instrument: NeckInstrument
) -> NeckPosition | int:
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (INeck): A neck instrument.

    Returns:
        NeckPosition: The position to play the notes on the instrument.
    """

    possible_positions = input_instrument.possible_positions(notes)
    possible_positions = [
        pos for pos in possible_positions if input_instrument.is_valid_position(pos)
    ]

    if len(possible_positions) == 0:
        return -1

    best_position = possible_positions[0]

    for position in possible_positions:
        if input_instrument.position_cost(position) < input_instrument.position_cost(best_position):
            best_position = position

    return best_position
