"""
This module provides the TimedChord class, which represents a chord with its timing information.
"""


class TimedChord:
    """
    Class representing a chord with its timing information.
    """

    def __init__(self, chord: tuple[int, ...], start_time: float, duration: float) -> None:
        """Initializes a TimedChord object.

        Args:
            chord (tuple[int, ...]): The chord being played, as a tuple of MIDI note numbers.
            start_time (float): The start time of the chord.
            duration (float): The duration of the chord.
        """
        self.__chord = chord
        self.__start_time = start_time
        self.__duration = duration

    def __str__(self) -> str:
        """Returns a string representation of the timed chord."""
        return (
            f"TimedChord(chord={self.__chord}, "
            f"start_time={self.__start_time}, "
            f"duration={self.__duration})"
        )

    def __repr__(self) -> str:
        """Returns a string representation of the timed chord."""
        return (
            f"TimedChord(chord={self.__chord!r}, "
            f"start_time={self.__start_time!r}, "
            f"duration={self.__duration!r})"
        )

    @property
    def chord(self) -> tuple[int, ...]:
        """Returns the chord being played."""
        return self.__chord

    @property
    def start_time(self) -> float:
        """Returns the start time of the chord."""
        return self.__start_time

    @property
    def duration(self) -> float:
        """Returns the duration of the chord."""
        return self.__duration
