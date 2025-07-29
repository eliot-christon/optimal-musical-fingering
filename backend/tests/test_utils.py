"""
This is the test suite for the utility functions of the musical instrument fingering application.
"""

import pytest

from backend.src.utils import constants
from backend.src.utils.note2num import note2num
from backend.src.utils.num2note import num2note
from backend.src.utils.roman_numerals import convert_to_roman


def test_note2num_conversion() -> None:
    """Test the note to MIDI number conversion."""
    assert note2num("C4") == 48
    assert note2num("D#5") == 63
    assert note2num("B4") == 59


def test_note2num_raises() -> None:
    """Test the note to MIDI number conversion raises errors."""
    with pytest.raises(KeyError):
        note2num("H4")


def test_num2note_conversion() -> None:
    """Test the MIDI number to note conversion."""
    assert num2note(60) == "C5"
    assert num2note(75) == "D#6"
    assert num2note(59) == "B4"
    assert isinstance(num2note(constants.MAX_MIDI_NOTE), str)


def test_num2note_raises() -> None:
    """Test the MIDI number to note conversion raises errors."""
    with pytest.raises(ValueError):
        num2note(constants.MAX_MIDI_NOTE + 1)
    with pytest.raises(ValueError):
        num2note(-1)


def test_roman_numerals_conversion() -> None:
    """Test the conversion to Roman numerals."""
    assert convert_to_roman(0) == "-"
    assert convert_to_roman(1) == "I"
    assert convert_to_roman(4) == "IV"
    assert convert_to_roman(5) == "V"
    assert convert_to_roman(10) == "X"
    assert isinstance(convert_to_roman(constants.MAX_ROMAN_NUMERAL), str)


def test_roman_numerals_raises() -> None:
    """Test the conversion to Roman numerals raises errors."""
    with pytest.raises(ValueError):
        convert_to_roman(-1)
    with pytest.raises(ValueError):
        convert_to_roman(constants.MAX_ROMAN_NUMERAL + 1)


def test_constants_module() -> None:
    """Test the constants module."""
    assert hasattr(constants, "MAX_ROMAN_NUMERAL")
    assert hasattr(constants, "MIN_ROMAN_NUMERAL")
    assert hasattr(constants, "MAX_MIDI_NOTE")
    assert hasattr(constants, "MIN_MIDI_NOTE")
    assert hasattr(constants, "MAX_ROMAN_NUMERAL")
    assert hasattr(constants, "MIN_ROMAN_NUMERAL")
    assert hasattr(constants, "MAX_MIDI_NOTE")
    assert hasattr(constants, "MIN_MIDI_NOTE")
