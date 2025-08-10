"""
This is the test suite for the neck arrangement functionality.
"""

from pathlib import Path

from pytest import raises

from backend.src.instruments.neck_instrument import Guitar
from backend.src.music_piece.music_piece import MusicPiece
from backend.src.music_piece.neck_arrangement import neck_arrangement
from backend.src.music_piece.timed_chord import TimedChord
from backend.src.positions.neck_position import NeckPosition


def test_neck_arrangement_basic() -> None:
    """Test basic neck arrangement functionality."""
    # Create a simple music piece with two chords (C major triad and G major triad in MIDI numbers)
    chord_1 = (48, 52, 55)
    chord_2 = (55, 59)
    tc1 = TimedChord(chord=chord_1, start_time=0.0, duration=1.0)
    tc2 = TimedChord(chord=chord_2, start_time=1.0, duration=1.0)
    piece = MusicPiece(title="Test Piece")
    piece.add_timed_chord(tc1)
    piece.add_timed_chord(tc2)

    instrument = Guitar()
    positions = neck_arrangement(music_piece=piece, instrument=instrument)

    assert isinstance(positions, list)
    assert len(positions) == 2
    for pos in positions:
        assert isinstance(pos, NeckPosition)
        assert instrument.is_valid_position(pos)


def test_neck_arrangement_from_midi() -> None:
    """Test neck arrangement functionality with a MIDI file."""
    midi_file_path = Path("backend/assets/midi_files/test_sample.mid")
    music_piece = MusicPiece.from_midi(midi_file_path)
    instrument = Guitar()
    with raises(ValueError):
        _ = neck_arrangement(music_piece=music_piece, instrument=instrument)
