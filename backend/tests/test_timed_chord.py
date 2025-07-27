"""
Unit tests for the TimedChord class, which represents a chord with timing information.
"""

import unittest

from src.music_piece.timed_chord import TimedChord


class TestTimedChord(unittest.TestCase):
    """
    Test suite for the TimedChord class.
    """

    def setUp(self) -> None:
        """
        Set up a TimedChord instance for testing.
        """
        self.chord = (60, 64, 67)  # C major chord in MIDI
        self.start_time = 1.5
        self.duration = 2.0
        self.timed_chord = TimedChord(self.chord, self.start_time, self.duration)

    def test_chord_property(self) -> None:
        """
        Test that the chord property returns the correct tuple of MIDI note numbers.
        """
        self.assertEqual(self.timed_chord.chord, self.chord)

    def test_start_time_property(self) -> None:
        """
        Test that the start_time property returns the correct start time value.
        """
        self.assertEqual(self.timed_chord.start_time, self.start_time)

    def test_duration_property(self) -> None:
        """
        Test that the duration property returns the correct duration value.
        """
        self.assertEqual(self.timed_chord.duration, self.duration)


if __name__ == "__main__":
    unittest.main()
