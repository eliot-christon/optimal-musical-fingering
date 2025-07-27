"""
Tests for the TimedChord class, which represents a chord with timing information.
"""

from src.music_piece.timed_chord import TimedChord

# Create a TimedChord instance for testing
chord = (60, 64, 67)  # C major chord in MIDI
START_TIME = 1.5
DURATION = 2.0
timed_chord = TimedChord(chord, START_TIME, DURATION)


def test_chord_property() -> None:
    """Test that the chord property returns the correct MIDI notes."""
    assert isinstance(timed_chord.chord, tuple)
    assert timed_chord.chord == chord


def test_start_time_property() -> None:
    """Test that the start_time property returns the correct start time."""
    assert timed_chord.start_time == START_TIME


def test_duration_property() -> None:
    """Test that the duration property returns the correct duration."""
    assert timed_chord.duration == DURATION
