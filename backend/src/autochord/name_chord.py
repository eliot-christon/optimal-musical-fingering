"""
This module aims to identify the name of a chord based on its notes.
It provides functionality to analyze the intervals between notes and determine the chord name.
"""

import json
from pathlib import Path

from src.utils.note2num import note2num
from src.utils.num2note import num2note

# Get the path to chord_data.json relative to this file using pathlib
CHORD_DATA_PATH = Path(__file__).parent / "chord_data.json"
with CHORD_DATA_PATH.open(encoding="utf-8") as f:
    chord_data = json.load(f)["intervals"]  # Assuming chord_data.json has an "intervals" key


def name_chord(in_notes: list[str] | list[int]) -> str:
    """Identifies the name of a chord based on its notes.

    Args:
        notes (list[str]): A list of note names (e.g., ['C4', 'E4', 'G4']).
        notes (list[int]): A list of MIDI note numbers (e.g., [60, 64, 67]).

    Returns:
        str: The name of the chord (e.g., 'Cm7b9').
    """
    if not in_notes:
        msg = "The input list of notes is empty."
        raise ValueError(msg)
    if len(in_notes) < 3:
        msg = "At least three notes are required to identify a chord."
        raise ValueError(msg)
    # Convert note names to MIDI numbers if necessary
    if isinstance(in_notes[0], str):
        notes = [note2num(note) for note in in_notes if isinstance(note, str)]
    else:
        notes = [int(note) for note in in_notes]

    # Sort the MIDI numbers
    notes.sort()

    # Identify intervals and determine chord name
    raw_intervals = [notes[i] - notes[0] for i in range(1, len(notes))]

    # simplify intervals if they are not in the chord_data
    intervals = [
        interval if str(interval) in chord_data else interval % 12 for interval in raw_intervals
    ]

    intervals.sort()  # Sort intervals for consistent naming
    # place the intervals 1, 2, 5 at the end to follow the chord naming convention
    for interval in [1, 2, 5]:
        if interval in intervals:
            intervals.remove(interval)
            intervals.append(interval)

    chord_name = num2note(notes[0])  # tonic note
    for num in range(10):
        chord_name = chord_name.replace(str(num), "")  # Remove any digit from the chord name

    for interval in intervals:
        chord_name += chord_data[str(interval)][1]

    return chord_name
