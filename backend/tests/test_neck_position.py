"""
This is the test suite for the neck position module of the musical instrument fingering application.
It tests the functionality of the neck position calculation based on musical notes.
"""

import unittest

from src.positions.neck_position import NeckPosition
from src.positions.position import Position


class TestNeckPosition(unittest.TestCase):
    """Test suite for the neck position module of the musical instrument fingering application."""

    def setUp(self) -> None:
        """Set up the test case with a default neck position."""
        self.neck_position_1 = NeckPosition(placements=[201, 402, 503], fingers=[1, 2, 3], pos_id=1)
        self.neck_position_2 = NeckPosition(placements=[110], fingers=[4])
        self.neck_position_3 = NeckPosition.from_strings_frets(
            fingers=[1, 2, 3], strings=[2, 4, 5], frets=[1, 2, 3], pos_id=1
        )
        self.neck_position_4 = NeckPosition.from_position(
            Position(placements=[201, 402, 503], fingers=[1, 2, 3], pos_id=1)
        )

    def test_neck_position_from_strings_frets(self) -> None:
        """Test the from_strings_frets method."""
        self.assertEqual(self.neck_position_3, self.neck_position_1)

    def test_neck_position_from_position(self) -> None:
        """Test the from_position method."""
        self.assertEqual(self.neck_position_4, self.neck_position_1)

    def test_neck_position_strings(self) -> None:
        """Test the strings property."""
        self.assertEqual(self.neck_position_1.strings, [2, 4, 5])
        self.assertEqual(self.neck_position_3.strings, [2, 4, 5])

    def test_neck_position_frets(self) -> None:
        """Test the frets property."""
        self.assertEqual(self.neck_position_1.frets, [1, 2, 3])
        self.assertEqual(self.neck_position_2.frets, [10])

    def test_neck_position_add_note(self) -> None:
        """Test adding a note to the neck position."""
        self.neck_position_2.add_note(string=3, fret=5, finger=4)
        self.assertIn(305, self.neck_position_2.placements)
        self.assertIn(4, self.neck_position_2.fingers)

    def test_neck_position_get_full_position(self) -> None:
        """Test getting the full position with a specified number of fingers."""
        full_position = self.neck_position_1.get_full_position(num_fingers=6)
        self.assertEqual(len(full_position.fingers), 3)
        self.assertEqual(full_position.placements, [-1, -1, 201, -1, 402, 503])
        self.assertRaises(ValueError, self.neck_position_1.get_full_position, num_fingers=2)

    def test_neck_position_shift(self) -> None:
        """Test shifting the neck position."""
        self.neck_position_1.shift(1)
        self.assertEqual(self.neck_position_1.placements, [201, 402, 503])
        self.assertEqual(self.neck_position_1.fingers, [2, 3, 4])

        with self.assertRaises(ValueError):
            self.neck_position_1.shift(1, max_finger=4)

        self.neck_position_1.shift(-1)
        self.assertEqual(self.neck_position_1.placements, [201, 402, 503])
        self.assertEqual(self.neck_position_1.fingers, [1, 2, 3])

    def test_neck_position_is_barre(self) -> None:
        """Test if the neck position is a barre."""
        self.assertFalse(self.neck_position_1.is_barre())
        barre_position = NeckPosition(placements=[201, 402, 503], fingers=[1, 1, 1])
        self.assertTrue(barre_position.is_barre())

    def test_neck_position_copy(self) -> None:
        """Test copying the neck position."""
        copied_position = self.neck_position_1.copy()
        self.assertEqual(copied_position, self.neck_position_1)
        self.assertIsNot(copied_position, self.neck_position_1)
