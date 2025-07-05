"""
This module contains the Instrument class,
which represents a musical instrument and its properties.
"""
__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import Tuple, Dict

from ..utils.note2num import note2num
from ..position import Position

class Instrument:
    """Class representing an instrument"""

    def __init__(self,
                 name:str,
                 family:str,
                 description:str,
                 note_range:Tuple[str, str],
                 # (min, max), 0 is the lowest note (C0), 127 is the highest note (G10)
                 fingers:Dict[int, str] = None
                 ):
        self.name = name
        self.family = family
        self.description = description
        self.range = (note2num(note_range[0]), note2num(note_range[1]))
        if fingers is None:
            self.fingers = {
                0: "left pinky",
                1: "left ring",
                2: "left middle",
                3: "left index",
                4: "left thumb",
                5: "right thumb",
                6: "right index",
                7: "right middle",
                8: "right ring",
                9: "right pinky"
            }
        else:
            self.fingers = fingers

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Instrument):
            return False
        for attr in self.__dict__:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def position_cost(self, position_1:Position) -> float:
        """Computes the cost of a position.
        In a keyboard instrument, the cost is for each hand
            . 0 when two fingers are below the ok distance
              (non overlapping <=> non negative distance)
            . the summed distance between the two fingers otherwise

        Args:
            position (Position): the position to evaluate
        """

    def transition_cost(self, position_1:Position, position_2:Position) -> float:
        """Computes the cost of a transition between two positions."""
