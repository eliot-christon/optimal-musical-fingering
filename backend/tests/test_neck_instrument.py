"""
This is the test file for the neck instrument module.
It tests the functionality of the NeckInstrument class and its methods.
"""

from backend.src.instruments.neck_instrument import NeckInstrument
from backend.src.positions.neck_position import NeckPosition
from backend.src.utils.note2num import note2num

untuned_strings = ["E2", "A2", "D3", "G3", "B3", "F4"]
untuned_guitar = NeckInstrument(
    name="Test Untuned Guitar",
    open_strings=untuned_strings,
    number_of_frets=14,
)
notes = [note2num(note) for note in ["C4", "E4", "G4"]]
possible_positions = untuned_guitar.possible_positions(notes)


def test_neck_instrument_initialization() -> None:
    """Test the initialization of a NeckInstrument object."""
    assert untuned_guitar.name == "Test Untuned Guitar"
    assert untuned_guitar.open_strings == [note2num(s) for s in untuned_strings]
    assert untuned_guitar.number_of_frets == 14


def test_neck_instrument_possible_positions() -> None:
    """Test the possible positions method of NeckInstrument."""
    assert isinstance(possible_positions, list)
    assert all(isinstance(pos, NeckPosition) for pos in possible_positions)
    assert len(possible_positions) > 0
    assert possible_positions[0].fingers != [0, 0, 0]
    # assert placements are 3 digits numbers
    assert all(len(str(placement)) == 3 for placement in possible_positions[0].placements)


def test_neck_instrument_is_valid_position() -> None:
    """Test the is_valid_position method of NeckInstrument."""
    valid_positions = [pos for pos in possible_positions if untuned_guitar.is_valid_position(pos)]
    assert len(valid_positions) <= len(possible_positions)
    # valid positions must have different strings
    assert all(len(set(pos.strings)) == len(pos.strings) for pos in valid_positions)


def test_neck_instrument_position_cost() -> None:
    """Test the position_cost method of NeckInstrument."""
    position = possible_positions[0]
    cost = untuned_guitar.position_cost(position)
    assert isinstance(cost, int)
    assert cost >= 0
