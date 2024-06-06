__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from ..Position import Position

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