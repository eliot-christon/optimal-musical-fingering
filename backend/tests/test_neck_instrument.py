"""
This is the test suite for the NeckInstrument class.
"""

from backend.src.instruments.neck_instrument import Banjo, Guitar, NeckInstrument
from backend.src.positions.neck_position import NeckPosition


def test_neck_instrument_default_initialization() -> None:
    """Test the default initialization of the NeckInstrument class."""
    instrument = NeckInstrument()
    assert instrument is not None
    assert instrument.open_strings is not None
    assert instrument.number_of_frets is not None
    assert instrument.fingers is not None
    assert instrument.name is not None
    assert instrument.family is not None
    assert instrument.description is not None
    assert isinstance(instrument.range, tuple) and len(instrument.range) == 2


random_neck_instrument_1 = NeckInstrument(
    open_strings=["E4", "A#2", "C3", "Gb3", "B4"],
    number_of_frets=6,
    fingers={0: "0", 1: "1", 2: "2", 3: "3"},
    name="Random Neck Instrument 1",
    description="A random neck instrument.",
)
guitar = Guitar()
banjo = Banjo()

neck_pos_1 = NeckPosition.from_strings_frets(fingers=[1, 2, 3], strings=[1, 2, 3], frets=[1, 2, 3])
neck_pos_2 = NeckPosition.from_strings_frets(fingers=[1, 2, 4], strings=[4, 5, 3], frets=[1, 2, 3])
neck_pos_3 = NeckPosition.from_strings_frets(
    fingers=[4, 3, 0, 0, 1, 2], strings=[1, 2, 3, 4, 5, 6], frets=[3, 3, 0, 0, 2, 3]
)
neck_pos_4 = NeckPosition.from_strings_frets(fingers=[2, 3, 4], strings=[1, 2, 3], frets=[1, 2, 3])


def test_neck_instrument_detail() -> None:
    """Test the details of the neck instruments."""
    detail_1 = random_neck_instrument_1.detail()
    assert isinstance(detail_1, dict)
    assert all(
        description_field in detail_1
        for description_field in [
            "description",
            "strings",
            "frets",
            "range",
        ]
    )


def test_neck_instrument_get_notes() -> None:
    """Test the get_notes method of the neck instruments."""
    assert guitar.get_notes(neck_pos_1) == ["F4", "C#4", "A#3"]
    assert guitar.get_notes(neck_pos_2) == ["D#3", "B2", "A#3"]
    assert guitar.get_notes(neck_pos_3) == ["G4", "D4", "G3", "D3", "B2", "G2"]
    assert banjo.get_notes(neck_pos_1) == ["D#4", "C#4", "A#3"]
    assert random_neck_instrument_1.get_notes(neck_pos_1) == ["F4", "C3", "D#3"]
    assert random_neck_instrument_1.get_notes(neck_pos_2) == [None, None, None]
    # None because the neck position is not valid for this instrument


def test_neck_instrument_is_valid_position() -> None:
    """Test the is_valid_position method of the neck instruments."""
    assert guitar.is_valid_position(neck_pos_1)
    assert guitar.is_valid_position(neck_pos_2)
    assert not banjo.is_valid_position(neck_pos_3)
    assert banjo.is_valid_position(neck_pos_1)
    assert random_neck_instrument_1.is_valid_position(neck_pos_1)
    assert not random_neck_instrument_1.is_valid_position(neck_pos_2)


def test_neck_instrument_default_fingering() -> None:
    """Test the default fingering of the neck instruments."""
    assert guitar.default_fingering(in_position=neck_pos_1) == neck_pos_1
    assert guitar.default_fingering(in_position=neck_pos_4) == neck_pos_1
    assert banjo.default_fingering(in_position=neck_pos_4) == neck_pos_1


def test_neck_instrument_position_cost() -> None:
    """Test the position cost of the neck instruments."""
    assert guitar.position_cost(neck_pos_4) > guitar.position_cost(neck_pos_1)
    assert guitar.position_cost(neck_pos_3) > guitar.position_cost(neck_pos_1)


def test_neck_instrument_possible_places_one_note() -> None:
    """Test the possible places for one note on the neck instruments."""
    assert guitar.possible_places_one_note(60) == [(2, 1), (3, 5), (4, 10)]
    assert not banjo.possible_places_one_note(100)


def test_neck_instrument_possible_positions() -> None:
    """Test the possible positions for notes on the neck instruments."""
    assert len(guitar.possible_positions([60])) > 3
    assert len(guitar.possible_positions([48, 50, 52])) > 0
    assert len(banjo.possible_positions([48, 50, 100])) == 0
