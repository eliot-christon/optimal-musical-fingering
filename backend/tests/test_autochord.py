"""
This is the test suite for the chord naming module of the musical instrument fingering application.
It tests the functionality of chord naming based on musical notes.
"""

import pytest
from src.autochord.name_chord import name_chord


def test_name_chord() -> None:
    """Test the naming of chords based on musical notes."""
    assert name_chord(["C4", "E4", "G4"]) == "C"
    assert name_chord(["D4", "F#4", "A4"]) == "D"
    assert name_chord(["C4", "Eb4", "G4"]) == "Cm"
    assert name_chord(["C4", "E4", "G4", "B4"]) == "Cmaj7"
    assert name_chord(["C4", "E4", "G4", "Bb4"]) == "C7"
    assert name_chord(["D2", "G2", "A3", "C4"]) == "D7sus4"
    assert name_chord(["F#3", "A3", "C#4", "E4"]) == "F#m7"
    assert name_chord(["C4", "E4", "Gb4", "F5"]) == "Cb511"
    assert name_chord(["Ab3", "C4", "Eb4", "G4"]) == "G#maj7"


def test_name_chord_with_midi_numbers() -> None:
    """Test the naming of chords based on MIDI numbers."""
    assert name_chord([60, 64, 67]) == "C"
    assert name_chord([62, 66, 69]) == "D"
    assert name_chord([60, 63, 67]) == "Cm"
    assert name_chord([60, 64, 67, 71]) == "Cmaj7"
    assert name_chord([60, 76, 67, 71]) == "Cmaj7"
    assert name_chord([60, 64, 67, 70]) == "C7"
    assert name_chord([60, 64, 67, 70, 73]) == "C7b9"
    assert name_chord([60, 64, 67, 74, 76]) == "C9"


def test_name_chord_raises() -> None:
    """Test the naming of chords raises errors for invalid input."""
    with pytest.raises(ValueError):
        name_chord([])
    with pytest.raises(KeyError):
        name_chord(["C4", "E4", "G4", "H4"])
    with pytest.raises(ValueError):
        name_chord(["C4", "E4"])
