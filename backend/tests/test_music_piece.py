"""
Tests for the MusicPiece class, which represents a musical piece with timed chords.
"""

from src.music_piece.music_piece import MusicPiece

PATH_TO_MIDI_FILE = "backend/assets/midi_files/sample_1.mid"


def test_music_piece_initialization() -> None:
    """Test the initialization of a MusicPiece object."""
    piece = MusicPiece(title="Test Piece", composer="Test Composer")
    assert piece.title == "Test Piece"
    assert piece.composer == "Test Composer"
    assert not piece.timed_chords


def test_music_piece_from_midi() -> None:
    """Test the creation of a MusicPiece object from a MIDI file."""
    piece = MusicPiece.from_midi(PATH_TO_MIDI_FILE)
    assert isinstance(piece, MusicPiece)
    assert piece.title == "Unknown Title"
    assert piece.composer == "Unknown Composer"
    assert len(piece.timed_chords) > 0
