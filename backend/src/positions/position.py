"""
This module contains the Position class,
which represent positions on musical instruments.
These classes provide methods for creating, manipulating,
and sorting positions based on placements and fingers.
"""

from collections.abc import Iterable
from typing import NamedTuple

from src.utils.note2num import note2num


class FingerPosition(NamedTuple):
    """Named tuple representing a finger position on an instrument.

    Attributes:
        placement (int): The MIDI note number of the placement.
        finger (int): The finger number associated with the placement.
    """

    placement: int
    finger: int


class Position:
    """Class representing a position on an instrument"""

    def __init__(
        self,
        finger_positions: Iterable[FingerPosition | tuple[int, int]],
        pos_id: int | None = None,
    ) -> None:
        """Initializes a Position object.

        Args:
            finger_positions (Iterable[FingerPosition]): An iterable of FingerPosition objects.
            pos_id (int|None): An optional identifier for the position.
        """
        self._finger_positions = [
            FingerPosition(*fp) if isinstance(fp, tuple) else fp for fp in finger_positions
        ]
        self._id = pos_id

    @classmethod
    def from_str_notes(cls, notes: list[str], fingers: list[int]) -> "Position":
        """Alternative constructor"""
        return cls(
            [
                FingerPosition(note2num(note), finger)
                for note, finger in zip(notes, fingers, strict=True)
            ]
        )

    def __str__(self) -> str:
        """Returns a string representation of the position"""
        return (
            "Hand Position:".join(
                f" {placement} (Finger {finger})"
                for placement, finger in zip(self.placements, self.fingers, strict=True)
            )
            + f" ID: {self._id if self._id is not None else 'None'}"
        )

    def __repr__(self) -> str:
        """Returns a string representation of the position"""
        return f"Position(finger_positions={self._finger_positions}, id={self._id})"

    def __len__(self) -> int:
        """Returns the number of placements in the position"""
        return len(self._finger_positions)

    def __hash__(self) -> int:
        """Returns a hash of the position"""
        return hash((self._finger_positions, self._id))

    def __eq__(self, other: object) -> bool:
        """Checks if two Position instances are equal"""
        if not isinstance(other, Position):
            return False
        return self._finger_positions == other._finger_positions and self._id == other._id

    @property
    def finger_positions(self) -> list[FingerPosition]:
        """Returns the finger positions of the position"""
        return self._finger_positions

    @property
    def placements(self) -> list[int]:
        """Returns the placements of the position"""
        return [fp.placement for fp in self._finger_positions if isinstance(fp, FingerPosition)]

    @property
    def fingers(self) -> list[int]:
        """Returns the fingers of the position"""
        return [fp.finger for fp in self._finger_positions if isinstance(fp, FingerPosition)]

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
        finger_positions = sorted(self._finger_positions, key=lambda x: x.finger)
        return Position(finger_positions, self._id)

    def sort_by_placement(self) -> "Position":
        """Sorts the placements and fingers by placement"""
        finger_positions = sorted(self._finger_positions, key=lambda x: x.placement)
        return Position(finger_positions, self._id)

    def get_full_position(self, num_fingers: int = 10) -> "Position":
        """Returns the full position (all fingers)
        quiet placements are represented by -1
        """
        if num_fingers < len(self._finger_positions):
            raise ValueError(
                f"num_fingers ({num_fingers}) must be greater than or equal"
                f" to the number of fingers in the position ({len(self._finger_positions)})"
            )
        new_finger_positions = []
        for i in range(num_fingers):
            if i in self.fingers:
                new_finger_positions.append(self._finger_positions[self.fingers.index(i)])
            else:
                new_finger_positions.append(FingerPosition(-1, i))
        return Position(new_finger_positions)

    def copy(self) -> "Position":
        """Returns a copy of the position"""
        return Position(self._finger_positions, self._id)
