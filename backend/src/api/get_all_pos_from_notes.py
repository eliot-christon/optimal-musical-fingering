"""
This module contains the logic for determining the optimal finger positions
for a given set of musical notes and a specific instrument.
"""

from backend.src.instruments.neck_instrument import NeckInstrument
from backend.src.positions.neck_position import NeckPosition


def get_all_pos_from_notes(
    notes: list[int], input_instrument: NeckInstrument
) -> dict[NeckPosition, float] | int:
    """
    This function takes a list of notes and an instrument and returns a position.

    Parameters:
        notes (List[str]): A list of notes.
        instrument (INeck): A neck instrument.

    Returns:
        dict[NeckPosition, int] | int: A dictionary mapping positions to their costs,
                                       or -1 if no valid positions are found.
    """

    possible_positions = input_instrument.possible_positions(notes)
    possible_positions = [
        pos for pos in possible_positions if input_instrument.is_valid_position(pos)
    ]

    if len(possible_positions) == 0:
        return -1

    positions_costs = {}
    for position in possible_positions:
        cost = input_instrument.position_cost(position)
        positions_costs[position] = cost

    return positions_costs
