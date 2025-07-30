"""
This is the test suite for the neck position module of the musical instrument fingering application.
It tests the functionality of the neck position calculation based on musical notes.
"""

import pytest
from src.positions.neck_position import NeckPosition
from src.positions.position import Position

# Define some sample neck positions for testing
neck_position_1 = NeckPosition(finger_positions=((201, 1), (402, 2), (503, 3)), pos_id=1)
neck_position_2 = NeckPosition(finger_positions=((110, 4),), pos_id=2)
neck_position_3 = NeckPosition.from_strings_frets(
    fingers=[1, 2, 3], strings=[2, 4, 5], frets=[1, 2, 3], pos_id=1
)
neck_position_4 = NeckPosition.from_position(
    Position(finger_positions=((201, 1), (402, 2), (503, 3)), pos_id=1)
)


def test_neck_position_from_strings_frets() -> None:
    """Test creating a NeckPosition from strings and frets."""
    assert neck_position_3 == neck_position_1


def test_neck_position_from_position() -> None:
    """Test creating a NeckPosition from a Position."""
    assert neck_position_4 == neck_position_1


def test_neck_position_strings() -> None:
    """Test the strings of the NeckPosition."""
    assert neck_position_1.strings == [2, 4, 5]
    assert neck_position_3.strings == [2, 4, 5]


def test_neck_position_frets() -> None:
    """Test the frets of the NeckPosition."""
    assert neck_position_1.frets == [1, 2, 3]
    assert neck_position_2.frets == [10]


def test_neck_position_add_note() -> None:
    """Test adding a note to the NeckPosition."""
    neck_position_2.add_note(string=3, fret=5, finger=4)
    assert 305 in neck_position_2.placements


def test_neck_position_get_full_position() -> None:
    """Test getting the full position with a specific number of fingers."""
    full_position = neck_position_1.get_full_position(num_fingers=6)
    assert len(full_position.fingers) == 6
    assert full_position.placements == [-1, -1, 201, -1, 402, 503]
    with pytest.raises(ValueError):
        neck_position_1.get_full_position(num_fingers=2)


def test_neck_position_shift() -> None:
    """Test shifting the NeckPosition."""
    neck_position = NeckPosition(finger_positions=((201, 1), (402, 2), (503, 3)), pos_id=1)
    neck_position.shift(1)
    assert neck_position.placements == [201, 402, 503]
    assert neck_position.fingers == [2, 3, 4]
    with pytest.raises(ValueError):
        neck_position.shift(1, max_finger=4)
    neck_position.shift(-1)
    assert neck_position.placements == [201, 402, 503]
    assert neck_position.fingers == [1, 2, 3]


def test_neck_position_is_barre() -> None:
    """Test if the NeckPosition is a barre."""
    neck_position = NeckPosition(finger_positions=((201, 1), (402, 2), (503, 3)), pos_id=1)
    assert not neck_position.is_barre()
    barre_position = NeckPosition(finger_positions=((201, 1), (402, 1), (503, 1)), pos_id=2)
    assert barre_position.is_barre()


def test_neck_position_copy() -> None:
    """Test copying the NeckPosition."""
    neck_position = NeckPosition(finger_positions=((201, 1), (402, 2), (503, 3)), pos_id=1)
    copied_position = neck_position.copy()
    assert copied_position == neck_position
    assert copied_position is not neck_position
