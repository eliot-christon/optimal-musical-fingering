"""
This is the test suite for the utility functions of the musical instrument fingering application.
"""

import unittest

from src.utils import constants
from src.utils.note2num import note2num
from src.utils.num2note import num2note
from src.utils.roman_numerals import convert_to_roman


class TestUtils(unittest.TestCase):
    """Test suite for the utility functions of the musical instrument fingering application."""

    def test_note2num_conversion(self) -> None:
        """Test the note2num function."""
        self.assertEqual(note2num("C4"), 48)
        self.assertEqual(note2num("D#5"), 63)
        self.assertEqual(note2num("B4"), 59)

    def test_note2num_raises(self) -> None:
        """Test the note2num raises ValueError for invalid inputs."""
        self.assertRaises(KeyError, note2num, "H4")

    def test_num2note_conversion(self) -> None:
        """Test the num2note function."""
        self.assertEqual(num2note(60), "C5")
        self.assertEqual(num2note(75), "D#6")
        self.assertEqual(num2note(59), "B4")
        self.assertIsInstance(num2note(constants.MAX_MIDI_NOTE), str)

    def test_num2note_raises(self) -> None:
        """Test the num2note raises ValueError for invalid inputs."""
        self.assertRaises(TypeError, num2note, 14.4)
        self.assertRaises(ValueError, num2note, constants.MAX_MIDI_NOTE + 1)
        self.assertRaises(ValueError, num2note, -1)

    def test_roman_numerals_conversion(self) -> None:
        """Test the roman_numerals function."""
        self.assertEqual(convert_to_roman(0), "-")
        self.assertEqual(convert_to_roman(1), "I")
        self.assertEqual(convert_to_roman(4), "IV")
        self.assertEqual(convert_to_roman(5), "V")
        self.assertEqual(convert_to_roman(10), "X")
        self.assertIsInstance(convert_to_roman(constants.MAX_ROMAN_NUMERAL), str)

    def test_roman_numerals_raises(self) -> None:
        """Test the roman_numerals raises ValueError for invalid inputs."""
        self.assertRaises(ValueError, convert_to_roman, -1)
        self.assertRaises(ValueError, convert_to_roman, constants.MAX_ROMAN_NUMERAL + 1)

    def test_constants(self) -> None:
        """Test the constants module."""
        self.assertTrue(hasattr(constants, "MAX_ROMAN_NUMERAL"))
        self.assertTrue(hasattr(constants, "MIN_ROMAN_NUMERAL"))
        self.assertTrue(hasattr(constants, "MAX_MIDI_NOTE"))
        self.assertTrue(hasattr(constants, "MIN_MIDI_NOTE"))
