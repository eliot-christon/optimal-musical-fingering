"""
Tests for the MusicPiece class, which represents a musical piece with timed chords.
"""

from backend.src.music_piece.music_piece import MusicPiece

PATH_TO_MIDI_FILE = "backend/assets/midi_files/test_sample.mid"


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
    assert piece.timed_chords[0].chord == (55, 63, 67, 70)
    assert piece.timed_chords[1].start_time - piece.timed_chords[0].start_time > 1
    assert piece.timed_chords[-1].chord == (51,)
    assert piece.timed_chords[-1].duration > 0.2
