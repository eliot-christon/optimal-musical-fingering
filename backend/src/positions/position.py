"""
This module contains the Position class,
which represent positions on musical instruments.
These classes provide methods for creating, manipulating,
and sorting positions based on placements and fingers.
"""
__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

from typing import List

from ..utils.note2num import note2num


class Position:
    """Class representing a position on an instrument"""

    def __init__(self, placements:List[int], fingers:List[int], pos_id:int=None):
        self.placements = list(placements)
        self.fingers = list(fingers)
        self.id = pos_id

    @classmethod
    def from_str_notes(cls, notes:List[str], fingers:List[int]):
        """Alternative constructor"""
        return cls([note2num(note) for note in notes], fingers)

    def __str__(self) -> str:
        return f"Placement: {self.placements}, Fingers: {self.fingers}, ID: {self.id}"

    def __repr__(self) -> str:
        return f"Position({self.placements}, {self.fingers}, {self.id})"

    def __len__(self) -> int:
        return len(self.placements)

    def sort_by_finger(self) -> "Position":
        """Sorts the placements and fingers by finger"""
        placements, fingers = map(list, zip(*sorted(
            zip(self.placements, self.fingers), key=lambda x: x[1])))
        return Position(placements, fingers, self.id)

    def sort_by_placement(self) -> "Position":
        """Sorts the placements and fingers by placement"""
        placements, fingers = map(list, zip(*sorted(
            zip(self.placements, self.fingers), key=lambda x: x[0])))
        return Position(placements, fingers, self.id)

    def get_full_position(self, num_fingers:int=10) ->  "Position":
        """Returns the full position (all fingers)
        quiet placements are represented by -1
        """
        new_placements = []
        new_fingers = [i for i in range(num_fingers)]
        for i in range(num_fingers):
            if i in self.fingers:
                new_placements.append(self.placements[self.fingers.index(i)])
            else:
                new_placements.append(-1)
        return Position(new_placements, new_fingers)

    def copy(self):
        """Returns a copy of the position"""
        return Position(self.placements.copy(), self.fingers.copy(), self.id)
