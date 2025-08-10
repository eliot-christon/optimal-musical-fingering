"""
This module provides functionality for working with music pieces, including
representation, and manipulation.
"""

from pretty_midi import PrettyMIDI

from backend.src.music_piece.timed_chord import TimedChord


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

    @classmethod
    def from_midi(cls, midi_file: str, fs: int = 20) -> "MusicPiece":
        """Creates a MusicPiece object from a MIDI file.

        Args:
            midi_file (str): The path to the MIDI file.
            fs (int): The frame rate.

        Returns:
            MusicPiece: An instance of MusicPiece created from the MIDI file.
        """
        midi_data = PrettyMIDI(midi_file)
        music_piece = cls(title="Unknown Title", composer="Unknown Composer")
        # first create a merged piano roll
        piano_roll = sum(instr.get_piano_roll(fs=fs) for instr in midi_data.instruments)
        # Convert to boolean (note present or not)
        note_on = piano_roll > 0
        # transpose
        note_on = note_on.T
        # Create timed chords from the piano roll
        previous_timed_chord = TimedChord(chord=(), start_time=0, duration=0)
        for time, column in enumerate(note_on):
            current_chord = tuple(pitch for pitch, is_on in enumerate(column) if is_on)
            if not current_chord:
                continue
            current_timed_chord = TimedChord(
                chord=current_chord, start_time=time / fs, duration=1 / fs
            )
            if previous_timed_chord.chord == current_timed_chord.chord:
                current_timed_chord.duration += previous_timed_chord.duration
                current_timed_chord.start_time = previous_timed_chord.start_time
            elif previous_timed_chord.chord:
                music_piece.add_timed_chord(previous_timed_chord)
            previous_timed_chord = current_timed_chord
        if current_timed_chord.chord:
            music_piece.add_timed_chord(current_timed_chord)
        return music_piece

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

    def add_timed_chord(self, timed_chord: TimedChord) -> None:
        """Adds a timed chord to the music piece."""
        self.__timed_chords.append(timed_chord)
