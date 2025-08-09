"""
This module contains the Neck Position class
which represent positions on musical instruments.
These classes provide methods for creating, manipulating,
and sorting positions based on placements and fingers.
"""

from backend.src.utils.roman_numerals import convert_to_roman

from .position import FingerPosition, Position


class NeckPosition(Position):
    """Class representing a position on a neck instrument.
    The position now gets a number of strings and frets"""

    @classmethod
    def from_strings_frets(
        cls, fingers: list[int], strings: list[int], frets: list[int], pos_id: int | None = None
    ) -> "NeckPosition":
        """Alternative constructor"""
        placements = cls.convert_strings_frets_to_placements(
            strings=list(strings), frets=list(frets)
        )
        finger_positions = [
            FingerPosition(placement, finger)
            for placement, finger in zip(placements, fingers, strict=True)
        ]
        return cls(finger_positions, pos_id)

    @classmethod
    def from_position(cls, position: Position) -> "NeckPosition":
        """Alternative constructor"""
        return cls(finger_positions=position.finger_positions, pos_id=position.id)

    def __str__(self) -> str:
        """Returns a string representation of the position"""
        roman_frets = [convert_to_roman(fret) for fret in self.frets]
        return (
            f"Strings: {self.strings}, Frets: {roman_frets}, Fingers: {self.fingers}, ID: {self.id}"
        )

    def __repr__(self) -> str:
        """Returns a string representation of the position"""
        return f"NPosition({self.strings}, {self.frets}, {self.fingers}, {self.id})"

    def to_json(self) -> dict:
        """Returns the position as a json"""
        return {
            "strings": self.strings,
            "frets": self.frets,
            "fingers": self.fingers,
            "id": self.id,
        }

    def sort_by_string(self, *, reverse: bool = True) -> "NeckPosition":
        """Sorts the placements and fingers by string"""
        sorted_finger_positions = sorted(
            self._finger_positions, key=lambda x: x.placement, reverse=reverse
        )
        return NeckPosition(sorted_finger_positions, self._id)

    def sort_by_fret(self) -> "NeckPosition":
        """Sorts the placements and fingers by fret"""
        sorted_finger_positions = sorted(self._finger_positions, key=lambda x: x.placement % 100)
        return NeckPosition(sorted_finger_positions, self._id)

    def sort_by_finger(self) -> "NeckPosition":
        """Sorts the placements and fingers by finger"""
        sorted_finger_positions = sorted(self._finger_positions, key=lambda x: x.finger)
        return NeckPosition(sorted_finger_positions, self._id)

    @staticmethod
    def convert_strings_frets_to_placements(strings: list[int], frets: list[int]) -> list[int]:
        """Converts a list of strings and frets to a list of placements.
        This assumes that there is less than 100 frets on one string."""
        return [string * 100 + fret for string, fret in zip(strings, frets, strict=False)]

    @property
    def strings(self) -> list[int]:
        """Returns the strings of the position"""
        return [note // 100 for note in self.placements]

    @property
    def frets(self) -> list[int]:
        """Returns the frets of the position"""
        return [note % 100 for note in self.placements]

    def add_note(self, string: int, fret: int, finger: int) -> None:
        """Adds a note to the position"""
        self._finger_positions.append(FingerPosition(string * 100 + fret, finger))

    def get_full_position(self, num_fingers: int = 6) -> "NeckPosition":
        """Returns the full position (all strings)
        quiet placements are represented by -1 (0 is playing the open string)
        """

        if num_fingers < len(self.fingers):
            msg = (
                "num_fingers must be greater than or equal to the number of fingers in the position"
            )
            raise ValueError(msg)

        num_strings = num_fingers  # assuming num_fingers is the number of strings
        new_finger_positions = []
        for i in range(num_strings):
            if i in self.strings:
                new_finger_positions.append(
                    FingerPosition(self.placements[self.strings.index(i)], i)
                )
            else:
                new_finger_positions.append(FingerPosition(-1, i))  # -1 for quiet placements
        return NeckPosition(new_finger_positions)

    def shift(self, shift: int, max_finger: int = 4) -> None:
        """Shifts the position by a number of fingers.
        Only non-quiet placements are shifted if max_finger doesn't occur in the position"""
        if max(self.fingers) + shift > max_finger:
            raise ValueError(
                f"Cannot shift position by {shift} fingers, "
                f"max finger {max_finger} would be exceeded."
            )
        if shift < 0 and min(self.fingers) + shift < 0:
            raise ValueError(
                f"Cannot shift position by {shift} fingers, "
                f"min finger {min(self.fingers)} would be exceeded."
            )
        self._finger_positions = [
            FingerPosition(fp.placement, fp.finger + shift) if fp.finger > 0 else fp
            for fp in self._finger_positions
        ]

    def is_barre(self) -> bool:
        """Returns True if the position is a barre.
        is barre when same finger > 0 on multiple strings"""
        non_quiet_fingers = [finger for finger in self.fingers if finger > 0]
        return len(non_quiet_fingers) != len(set(non_quiet_fingers))

    def copy(self) -> "NeckPosition":
        """Returns a copy of the position"""
        return NeckPosition(self._finger_positions.copy(), self._id)
