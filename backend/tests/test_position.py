"""
This is the test suite for the position module of the musical instrument fingering application.
It tests the functionality of the position calculation based on musical notes.
"""

import unittest

from src.positions.position import Position


class TestPosition(unittest.TestCase):
    """Test suite for the position module of the musical instrument fingering application."""

    def setUp(self) -> None:
        """Set up the test case with a default position."""
        self.position_1 = Position(placements=[48, 52, 55], fingers=[1, 2, 3], pos_id=1)
        self.position_2 = Position(placements=[48, 55, 52], fingers=[4, 2, 1])
        self.position_3 = Position.from_str_notes(["C4", "E4", "G4"], [1, 2, 3])
        self.position_3.id = 1

    def test_position_basics(self) -> None:
        """Test the basic functionality of the Position class."""
        self.assertIsInstance(self.position_1, Position)
        self.assertEqual(len(self.position_1.fingers), 3)

    def test_position_from_str_notes(self) -> None:
        """Test the equality of two Position instances, one created from string notes."""
        self.assertEqual(self.position_1, self.position_3)

    def test_position_sort_by_finger(self) -> None:
        """Test the sorting of positions by finger."""
        sorted_position = self.position_2.sort_by_finger()
        self.assertEqual(sorted_position.fingers, [1, 2, 4])
        self.assertEqual(sorted_position.placements, [52, 55, 48])

    def test_position_sort_by_placement(self) -> None:
        """Test the sorting of positions by placement."""
        sorted_position = self.position_2.sort_by_placement()
        self.assertEqual(sorted_position.placements, [48, 52, 55])
        self.assertEqual(sorted_position.fingers, [4, 1, 2])

    def test_position_get_full_position_1(self) -> None:
        """Test the get_full_position method."""
        full_position = self.position_2.get_full_position(num_fingers=5)
        self.assertEqual(full_position.placements, [-1, 52, 55, -1, 48])
        self.assertEqual(full_position.fingers, [0, 1, 2, 3, 4])

    def test_position_get_full_position_2(self) -> None:
        """Test the get_full_position method with a different number of fingers."""
        full_position = self.position_2.get_full_position(num_fingers=10)
        self.assertEqual(len(full_position.fingers), 10)
        self.assertEqual(len(full_position.placements), 10)

    def test_position_get_full_position_raise_error(self) -> None:
        """Test that get_full_position raises an error for invalid number of fingers."""
        self.assertRaises(ValueError, self.position_2.get_full_position, num_fingers=-1)
        self.assertRaises(ValueError, self.position_2.get_full_position, num_fingers=2)
