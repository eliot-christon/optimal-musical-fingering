"""
This module contains the Position class,
which represent positions on musical instruments.
These classes provide methods for creating, manipulating,
and sorting positions based on placements and fingers.
"""

from src.utils.note2num import note2num


class Position:
    """Class representing a position on an instrument"""

    def __init__(
        self, placements: list[int], fingers: list[int], pos_id: int | None = None
    ) -> None:
        """Initializes a Position object.

        Args:
            placements (list[int]): A list of placements (midi note numbers).
            fingers (list[int]): A list of integers corresponding to the finger placements.
            pos_id (int|None): An optional identifier for the position.
        """
        self._placements = list(placements)
        self._fingers = list(fingers)
        self._id = pos_id

    @classmethod
    def from_str_notes(cls, notes: list[str], fingers: list[int]) -> "Position":
        """Alternative constructor"""
        return cls([note2num(note) for note in notes], fingers)

    def __str__(self) -> str:
        """Returns a string representation of the position"""
        return f"Placement: {self._placements}, Fingers: {self._fingers}, ID: {self._id}"

    def __repr__(self) -> str:
        """Returns a string representation of the position"""
        return f"Position({self._placements}, {self._fingers}, {self._id})"

    def __len__(self) -> int:
        """Returns the number of placements in the position"""
        return len(self._placements)

    def __hash__(self) -> int:
        """Returns a hash of the position"""
        return hash((tuple(self._placements), tuple(self._fingers), self._id))

    def __eq__(self, other: object) -> bool:
        """Checks if two Position instances are equal"""
        if not isinstance(other, Position):
            return False
        return (
            self._placements == other._placements
            and self._fingers == other._fingers
            and self._id == other._id
        )

    @property
    def placements(self) -> list[int]:
        """Returns the placements of the position"""
        return self._placements

    @property
    def fingers(self) -> list[int]:
        """Returns the fingers of the position"""
        return self._fingers

    @property
    def id(self) -> int | None:
        """Returns the ID of the position"""
        return self._id

    @id.setter
    def id(self, value: int | None) -> None:
        """Sets the ID of the position"""
        self._id = value

    def sort_by_finger(self) -> "Position":
        """Sorts the placements and fingers by finger"""
        placements, fingers = map(
            list,
            zip(
                *sorted(zip(self._placements, self._fingers, strict=False), key=lambda x: x[1]),
                strict=False,
            ),
        )
        return Position(placements, fingers, self._id)

    def sort_by_placement(self) -> "Position":
        """Sorts the placements and fingers by placement"""
        placements, fingers = map(
            list,
            zip(
                *sorted(zip(self._placements, self._fingers, strict=False), key=lambda x: x[0]),
                strict=False,
            ),
        )
        return Position(placements, fingers, self._id)

    def get_full_position(self, num_fingers: int = 10) -> "Position":
        """Returns the full position (all fingers)
        quiet placements are represented by -1
        """
        if num_fingers < len(self._fingers):
            raise ValueError(
                f"num_fingers ({num_fingers}) must be greater than or equal"
                f" to the number of fingers in the position ({len(self._fingers)})"
            )
        new_placements = []
        new_fingers = list(range(num_fingers))
        for i in range(num_fingers):
            if i in self._fingers:
                new_placements.append(self._placements[self._fingers.index(i)])
            else:
                new_placements.append(-1)
        return Position(new_placements, new_fingers)

    def copy(self) -> "Position":
        """Returns a copy of the position"""
        return Position(self._placements.copy(), self._fingers.copy(), self._id)
