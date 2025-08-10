"""
This module provides functionality for arranging musical pieces.
The idea is to create a playable arrangement of a music piece
based on the positions available for a given neck instrument.
"""

from backend.src.instruments.neck_instrument import NeckInstrument
from backend.src.music_piece.music_piece import MusicPiece
from backend.src.positions.neck_position import NeckPosition
from backend.src.utils.num2note import num2note


def neck_arrangement(music_piece: MusicPiece, instrument: NeckInstrument) -> list[NeckPosition]:
    """Arranges the music piece for the specified instrument.
    Taking into account:
        - position cost
        - transition cost
    """
    positions = []
    for timed_chord in music_piece.timed_chords:
        notes = list(timed_chord.chord)
        possible_pos = instrument.possible_positions(notes)
        if len(possible_pos) == 0:
            raise ValueError(f"No positions found for notes: {notes} for {instrument}")
        possible_pos = [pos for pos in possible_pos if instrument.is_valid_position(pos)]

        if len(possible_pos) == 0:
            notes_str = ", ".join([num2note(note) for note in notes])
            raise ValueError(f"No valid positions found for notes: {notes_str} for {instrument}")

        # no logic for now, just taking any position
        positions.append(possible_pos[0])
    return positions
