"""
This module contains the Neck Position class
which represent positions on musical instruments.
These classes provide methods for creating, manipulating,
and sorting positions based on placements and fingers.
"""

__author__ = "Eliot Christon"
__email__ = "eliot.christon@gmail.com"
__github__ = "eliot-christon"


from src.utils.roman_numerals import convert_to_roman

from .position import Position


class NeckPosition(Position):
    """Class representing a position on a neck instrument.
    The position now gets a number of strings and frets"""

    def __init__(
        self, placements: list[int], fingers: list[int], pos_id: int | None = None
    ) -> None:
        """Initializes a NeckPosition object.

        Args:
            placements (list[int]): A list of placements (midi note numbers).
            fingers (list[int]): A list of fingers corresponding to the placements.
            pos_id (int|None): An optional identifier for the position.
        """
        super().__init__(list(placements), list(fingers), pos_id)

    @classmethod
    def from_strings_frets(
        cls, fingers: list[int], strings: list[int], frets: list[int], pos_id: int | None = None
    ) -> "NeckPosition":
        """Alternative constructor"""
        placements = cls.convert_strings_frets_to_placements(
            None, strings=list(strings), frets=list(frets)
        )
        return cls(placements, list(fingers), pos_id)

    @classmethod
    def from_position(cls, position: Position) -> "NeckPosition":
        """Alternative constructor"""
        return cls(position.placements, position.fingers, position.id)

    def __str__(self) -> str:
        """Returns a string representation of the position"""
        roman_frets = [convert_to_roman(fret) for fret in self.frets]
        return (
            f"Strings: {self.strings}, Frets: {roman_frets}, Fingers: {self.fingers}, ID: {self.id}"
        )

    def __repr__(self) -> str:
        """Returns a string representation of the position"""
        return f"NPosition({self.placements}, {self.fingers}, {self.id})"

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
        sorted_placements, sorted_fingers = map(
            list,
            zip(
                *sorted(
                    zip(self.placements, self.fingers, strict=False),
                    key=lambda x: x[0],
                    reverse=reverse,
                ),
                strict=False,
            ),
        )
        return NeckPosition(sorted_placements, sorted_fingers, self.id)

    def sort_by_fret(self) -> "NeckPosition":
        """Sorts the placements and fingers by fret"""
        sorted_placements, sorted_fingers = map(
            list,
            zip(
                *sorted(zip(self.placements, self.fingers, strict=False), key=lambda x: x[0] % 100),
                strict=False,
            ),
        )
        return NeckPosition(sorted_placements, sorted_fingers, self.id)

    def sort_by_finger(self) -> "NeckPosition":
        """Sorts the placements and fingers by finger"""
        placements, fingers = map(
            list,
            zip(
                *sorted(zip(self.placements, self.fingers, strict=False), key=lambda x: x[1]),
                strict=False,
            ),
        )
        return NeckPosition(placements, fingers, self.id)

    def convert_strings_frets_to_placements(
        self, strings: list[int], frets: list[int]
    ) -> list[int]:
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
        self.placements.append(string * 100 + fret)
        self.fingers.append(finger)

    def get_full_position(self, num_fingers: int = 6) -> "NeckPosition":
        """Returns the full position (all strings)
        quiet placements are represented by -1 (0 is playing the open string)
        """
        num_strings = num_fingers  # assuming num_fingers is the number of strings
        new_placements = []
        for i in range(num_strings):
            if i in self.strings:
                new_placements.append(self.placements[self.strings.index(i)])
            else:
                new_placements.append(-1)
        return NeckPosition(new_placements, self.fingers)

    def shift(self, shift: int, max_finger: int = 4) -> None:
        """Shifts the position by a number of fingers.
        Only non-quiet placements are shifted if max_finger doesn't occur in the position"""
        if max_finger in self.fingers or max(self.fingers) + shift > max_finger:
            return
        # if finger > 0, shift finger
        new_fingers = []
        for i in range(len(self.placements)):
            if self.fingers[i] > 0:
                new_fingers.append(self.fingers[i] + shift)
            else:
                new_fingers.append(self.fingers[i])
        self.fingers = new_fingers

    def is_barre(self) -> bool:
        """Returns True if the position is a barre.
        is barre when same finger > 0 on multiple strings"""
        non_quiet_fingers = [finger for finger in self.fingers if finger > 0]
        return len(non_quiet_fingers) != len(set(non_quiet_fingers))

    def copy(self) -> "NeckPosition":
        """Returns a copy of the position"""
        return NeckPosition(self.placements.copy(), self.fingers.copy(), self.id)
