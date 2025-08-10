"""
This module provides functionality for working with piano rolls.
"""

from collections.abc import Iterable
from pathlib import Path

import pretty_midi


class PianoRoll:
    """
    A PianoRoll is a representation of musical notes over time, where rows correspond to pitches
    and columns correspond to time frames.

    The roll is a 2D array where each element is a boolean indicating the presence of a note.
    """

    def __init__(self, roll: Iterable[Iterable[bool]], frame_rate: int = 20) -> None:
        """Initializes a PianoRoll object. Always stores roll as a list of lists."""
        self.__roll = [list(row) for row in roll]
        self.frame_rate = frame_rate

    @classmethod
    def from_midi(cls, midi_path: Path, fs: int = 20) -> "PianoRoll":
        """
        Creates a PianoRoll object from a MIDI file.
        """
        midi_data = pretty_midi.PrettyMIDI(midi_path.as_posix())

        # Merge all instruments into one piano roll
        piano_roll = sum(instr.get_piano_roll(fs=fs) for instr in midi_data.instruments)

        # Convert to boolean (note present or not)
        note_on = piano_roll > 0

        return cls(roll=note_on, frame_rate=fs)

    @property
    def roll(self) -> list[list[bool]]:
        """Returns the piano roll as a 2D list."""
        return self.__roll

    @property
    def transposed_roll(self) -> list[list[bool]]:
        """Returns the transposed version of the piano roll."""
        return [list(row) for row in zip(*self.__roll, strict=False)]

    def to_ascii(self) -> str:
        """
        Converts the piano roll to an ASCII representation.
        """
        # reverse the roll so high notes are at the top
        reversed_roll = self.__roll[::-1]
        return "\n".join("".join("#" if col else "." for col in row) for row in reversed_roll)
