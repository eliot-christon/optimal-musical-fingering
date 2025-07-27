"""
This module provides functionality for working with music pieces, including
representation, and manipulation.
"""

from src.music_piece.timed_chord import TimedChord


class MusicPiece:
    """
    Class representing a music piece.
    A music piece represents a collection of chords or single notes (timed chords).

    optionally:
        - The title of the piece
        - The composer of the piece
    """

    def __init__(self, title: str = "", composer: str = "") -> None:
        """Initializes a MusicPiece object.

        Args:
            title (str): The title of the music piece.
            composer (str): The composer of the music piece.
        """
        self.__title = title
        self.__composer = composer
        self.__timed_chords: list[TimedChord] = []

        # @classmethod
        # def from_midi(cls, midi_file: str) -> "MusicPiece":
        """Creates a MusicPiece object from a MIDI file.

        Args:
            midi_file (str): The path to the MIDI file.

        Returns:
            MusicPiece: An instance of MusicPiece created from the MIDI file.
        """

    def __str__(self) -> str:
        """Returns a string representation of the music piece."""
        return f"MusicPiece(title={self.__title}, composer={self.__composer})"

    def __repr__(self) -> str:
        """Returns a string representation of the music piece."""
        return f"MusicPiece(title={self.__title!r}, composer={self.__composer!r})"

    @property
    def title(self) -> str:
        """Returns the title of the music piece."""
        return self.__title

    @property
    def composer(self) -> str:
        """Returns the composer of the music piece."""
        return self.__composer

    @property
    def timed_chords(self) -> list[TimedChord]:
        """Returns the timed chords of the music piece."""
        return self.__timed_chords
