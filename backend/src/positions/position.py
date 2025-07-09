"""
This module contains the Position class,
which represent positions on musical instruments.
These classes provide methods for creating, manipulating,
and sorting positions based on placements and fingers.
"""

__author__ = "Eliot Christon"
__email__ = "eliot.christon@gmail.com"
__github__ = "eliot-christon"


from src.utils.note2num import note2num


class Position:
    """Class representing a position on an instrument"""

    def __init__(
        self, placements: list[int], fingers: list[int], pos_id: int | None = None
    ) -> None:
        """Initializes a Position object.

        Args:
            placements (list[int]): A list of placements (midi note numbers).
            fingers (list[int]): A list of fingers corresponding to the placements.
            pos_id (int|None): An optional identifier for the position.
        """
        self.placements = list(placements)
        self.fingers = list(fingers)
        self.id = pos_id

    @classmethod
    def from_str_notes(cls, notes: list[str], fingers: list[int]) -> "Position":
        """Alternative constructor"""
        return cls([note2num(note) for note in notes], fingers)

    def __str__(self) -> str:
        """Returns a string representation of the position"""
        return f"Placement: {self.placements}, Fingers: {self.fingers}, ID: {self.id}"

    def __repr__(self) -> str:
        """Returns a string representation of the position"""
        return f"Position({self.placements}, {self.fingers}, {self.id})"

    def __len__(self) -> int:
        """Returns the number of placements in the position"""
        return len(self.placements)

    def sort_by_finger(self) -> "Position":
        """Sorts the placements and fingers by finger"""
        placements, fingers = map(
            list,
            zip(
                *sorted(zip(self.placements, self.fingers, strict=False), key=lambda x: x[1]),
                strict=False,
            ),
        )
        return Position(placements, fingers, self.id)

    def sort_by_placement(self) -> "Position":
        """Sorts the placements and fingers by placement"""
        placements, fingers = map(
            list,
            zip(
                *sorted(zip(self.placements, self.fingers, strict=False), key=lambda x: x[0]),
                strict=False,
            ),
        )
        return Position(placements, fingers, self.id)

    def get_full_position(self, num_fingers: int = 10) -> "Position":
        """Returns the full position (all fingers)
        quiet placements are represented by -1
        """
        new_placements = []
        new_fingers = list(range(num_fingers))
        for i in range(num_fingers):
            if i in self.fingers:
                new_placements.append(self.placements[self.fingers.index(i)])
            else:
                new_placements.append(-1)
        return Position(new_placements, new_fingers)

    def copy(self) -> "Position":
        """Returns a copy of the position"""
        return Position(self.placements.copy(), self.fingers.copy(), self.id)
