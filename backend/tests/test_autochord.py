"""
This is the test suite for the chord naming module of the musical instrument fingering application.
It tests the functionality of chord naming based on musical notes.
"""

import unittest

from src.autochord.name_chord import name_chord


class TestNameChord(unittest.TestCase):
    """Test suite for the chord naming module of the musical instrument fingering application."""

    def test_name_chord(self) -> None:
        """Test the name_chord function with various inputs."""
        self.assertEqual(name_chord(["C4", "E4", "G4"]), "C")
        self.assertEqual(name_chord(["D4", "F#4", "A4"]), "D")
        self.assertEqual(name_chord(["C4", "Eb4", "G4"]), "Cm")
        self.assertEqual(name_chord(["C4", "E4", "G4", "B4"]), "Cmaj7")
        self.assertEqual(name_chord(["C4", "E4", "G4", "Bb4"]), "C7")
        self.assertEqual(name_chord(["D2", "G2", "A3", "C4"]), "D7sus4")
        self.assertEqual(name_chord(["F#3", "A3", "C#4", "E4"]), "F#m7")
        self.assertEqual(name_chord(["C4", "E4", "Gb4", "F5"]), "Cb511")
        self.assertEqual(name_chord(["Ab3", "C4", "Eb4", "G4"]), "G#maj7")

    def test_name_chord_with_midi_numbers(self) -> None:
        """Test the name_chord function with MIDI note numbers."""
        self.assertEqual(name_chord([60, 64, 67]), "C")
        self.assertEqual(name_chord([62, 66, 69]), "D")
        self.assertEqual(name_chord([60, 63, 67]), "Cm")
        self.assertEqual(name_chord([60, 64, 67, 71]), "Cmaj7")
        self.assertEqual(name_chord([60, 76, 67, 71]), "Cmaj7")
        self.assertEqual(name_chord([60, 64, 67, 70]), "C7")
        self.assertEqual(name_chord([60, 64, 67, 70, 73]), "C7b9")
        self.assertEqual(name_chord([60, 64, 67, 74, 76]), "C9")

    def test_name_chord_raises(self) -> None:
        """Test that name_chord raises ValueError for different invalid inputs."""
        self.assertRaises(ValueError, name_chord, [])
        self.assertRaises(KeyError, name_chord, ["C4", "E4", "G4", "H4"])
        self.assertRaises(ValueError, name_chord, ["C4", "E4"])
