"""
This is the test suite for the position module of the musical instrument fingering application.
It tests the functionality of the position calculation based on musical notes.
"""

import pytest

from backend.src.positions.position import Position

# Define some sample positions for testing
position_1 = Position(finger_positions=((60, 1), (64, 2), (67, 3)), pos_id=1)
position_2 = Position(finger_positions=((60, 4), (67, 2), (64, 1)), pos_id=2)
position_3 = Position.from_str_notes(["C4", "E4", "G4"], [1, 2, 3])
position_3.id = 1


def test_position_basics() -> None:
    """Test basic properties of the Position class."""
    assert isinstance(position_1, Position)
    assert len(position_1.fingers) == 3


def test_position_from_str_notes() -> None:
    """Test creating a Position from string notes."""
    assert position_1 == position_3


def test_position_sort_by_finger() -> None:
    """Test sorting the position by finger."""
    sorted_position = position_2.sort_by_finger()
    assert sorted_position.fingers == [1, 2, 4]
    assert sorted_position.placements == [64, 67, 60]


def test_position_sort_by_placement() -> None:
    """Test sorting the position by placement."""
    sorted_position = position_2.sort_by_placement()
    assert sorted_position.placements == [60, 64, 67]
    assert sorted_position.fingers == [4, 1, 2]


def test_position_get_full_position_2() -> None:
    """Test getting the full position with a specific number of fingers."""
    full_position = position_2.get_full_position(num_fingers=10)
    assert len(full_position.fingers) == 10
    assert len(full_position.placements) == 10


def test_position_get_full_position_raise_error() -> None:
    """Test getting the full position raises errors for invalid input."""
    with pytest.raises(ValueError):
        position_2.get_full_position(num_fingers=-1)
    with pytest.raises(ValueError):
        position_2.get_full_position(num_fingers=2)
