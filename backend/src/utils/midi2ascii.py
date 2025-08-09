"""
This module contains functions for converting MIDI files to ASCII representations.
"""

import pretty_midi


def midi2ascii(midi_path: str, fs: int = 20) -> str:
    """
    Converts a MIDI file to its ASCII piano roll representation.
    fs: int is the frames per second for the piano roll resolution.
    """
    midi_data = pretty_midi.PrettyMIDI(midi_path)

    # Merge all instruments into one piano roll
    piano_roll = sum(instr.get_piano_roll(fs=fs) for instr in midi_data.instruments)

    # Convert to boolean (note present or not)
    note_on = piano_roll > 0

    # Reverse so top of file = highest pitch
    note_on = note_on[::-1]

    return "\n".join("".join("#" if col else "." for col in row) for row in note_on)
