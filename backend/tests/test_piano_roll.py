"""
This is the test suite for the PianoRoll class.
"""

from pathlib import Path

from backend.src.music_piece.piano_roll import PianoRoll

PATH_TO_MIDI_FILE = Path("backend/assets/midi_files/test_sample3.mid")

basic_roll = [[False, True, False, False], [True, True, False, False], [False, True, True, False]]


def test_piano_roll_initialization() -> None:
    """Test the initialization of a PianoRoll object."""
    piano_roll = PianoRoll(roll=basic_roll, frame_rate=30)
    assert piano_roll.roll == basic_roll
    assert piano_roll.frame_rate == 30


def test_piano_roll_from_midi() -> None:
    """Test the creation of a PianoRoll object from a MIDI file."""
    piano_roll = PianoRoll.from_midi(PATH_TO_MIDI_FILE)
    assert isinstance(piano_roll, PianoRoll)
    assert piano_roll.frame_rate == 20
    assert len(piano_roll.roll) == 128


def test_transposed_roll() -> None:
    """Test the transposed version of the piano roll."""
    piano_roll = PianoRoll(roll=basic_roll, frame_rate=30)
    transposed = piano_roll.transposed_roll
    assert len(transposed) == 4
    assert len(transposed[0]) == 3
    assert transposed == [
        [False, True, False],
        [True, True, True],
        [False, False, True],
        [False, False, False],
    ]
