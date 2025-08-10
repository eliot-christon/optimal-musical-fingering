"""
This module provides functionality for working with music pieces, including
representation, and manipulation.
"""

from pathlib import Path

from backend.src.music_piece.piano_roll import PianoRoll
from backend.src.music_piece.timed_chord import TimedChord


class MusicPiece:
    """
    Class representing a music piece.
    A music piece represents a collection of chords or single notes (timed chords).

    optionally:
        - The title of the piece
    """

    def __init__(self, title: str = "") -> None:
        """Initializes a MusicPiece object.

        Args:
            title (str): The title of the music piece.
        """
        self.__title = title
        self.__timed_chords: list[TimedChord] = []

    @classmethod
    def from_roll(cls, roll: PianoRoll, title: str = "") -> "MusicPiece":
        """Creates a MusicPiece object from a piano roll.

        Args:
            roll (PianoRoll): The piano roll representation.
            title (str): The title of the music piece.

        Returns:
            MusicPiece: An instance of MusicPiece created from the piano roll.
        """
        music_piece = cls(title=title)

        # Create timed chords from the piano roll
        previous_timed_chord = TimedChord(chord=(), start_time=0, duration=0)

        for index, column in enumerate(roll.transposed_roll):
            current_chord = tuple(pitch for pitch, is_on in enumerate(column) if is_on)
            if not current_chord:
                continue
            current_timed_chord = TimedChord(
                chord=current_chord,
                start_time=index / roll.frame_rate,
                duration=1 / roll.frame_rate,
            )
            if previous_timed_chord.chord == current_timed_chord.chord:
                # if chords are the same, extend the duration of the previous chord
                current_timed_chord = previous_timed_chord
                current_timed_chord.duration += 1 / roll.frame_rate
            elif previous_timed_chord.is_not_empty():
                # if chords are different and a previous chord exists, add it to the music piece
                music_piece.add_timed_chord(previous_timed_chord)
            previous_timed_chord = current_timed_chord

        # Add the last timed chord if it exists at the last index
        if current_timed_chord.is_not_empty():
            music_piece.add_timed_chord(current_timed_chord)

        return music_piece

    @classmethod
    def from_midi(cls, midi_path: Path, fs: int = 20) -> "MusicPiece":
        """Creates a MusicPiece object from a MIDI file.

        Args:
            midi_file (Path): The path to the MIDI file.
            fs (int): The frame rate.

        Returns:
            MusicPiece: An instance of MusicPiece created from the MIDI file.
        """
        # Create a piano roll from the MIDI file
        piano_roll = PianoRoll.from_midi(midi_path, fs=fs)
        # Convert the piano roll to timed chords
        return cls.from_roll(piano_roll, title=midi_path.stem)

    def __str__(self) -> str:
        """Returns a string representation of the music piece."""
        return f"MusicPiece(title={self.__title})"

    def __repr__(self) -> str:
        """Returns a string representation of the music piece."""
        return f"MusicPiece(title={self.__title!r})"

    @property
    def title(self) -> str:
        """Returns the title of the music piece."""
        return self.__title

    @property
    def timed_chords(self) -> list[TimedChord]:
        """Returns the timed chords of the music piece."""
        return self.__timed_chords

    def add_timed_chord(self, timed_chord: TimedChord) -> None:
        """Adds a timed chord to the music piece."""
        self.__timed_chords.append(timed_chord)
