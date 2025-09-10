"""
This module retrieves optimal finger positions for given music piece and instrument.
"""

from pathlib import Path

from backend.src.instruments.neck_instrument import NeckInstrument
from backend.src.music_piece.arrangement.build_position_graph import build_position_graph
from backend.src.music_piece.arrangement.dijkstra import DijkstraResult, dijkstra
from backend.src.music_piece.music_piece import MusicPiece
from backend.src.positions.neck_position import NeckPosition


def midi2optimal_positions(
    midi_file_path: Path, instrument: NeckInstrument, midi_frame_rate: int = 20
) -> list[NeckPosition]:
    """
    This function takes a MIDI file path and an instrument, and returns a list of optimal positions.

    Parameters:
        midi_file_path (Path): The path to the MIDI file.
        instrument (NeckInstrument): The instrument for which to find optimal positions.

    Returns:
        List[NeckPosition]: A list of optimal finger positions for the music piece.
    """
    music_piece = MusicPiece().from_midi(midi_file_path, fs=midi_frame_rate)

    graph, error_messages = build_position_graph(music_piece, instrument)
    if error_messages:
        raise ValueError(f"Errors in building position graph: {error_messages}")

    start_node_id = -1  # Assuming -1 is the ID for the start node
    terminal_node_id = -2  # Assuming -2 is the ID for the terminal node
    dijkstra_result: DijkstraResult = dijkstra(graph, start_node_id)

    path_node_ids = dijkstra_result.get_path(terminal_node_id)
    return [
        NeckPosition.from_placement_code(node_id // 1000)
        for node_id in path_node_ids
        if node_id >= 0  # Exclude start and terminal nodes
    ]
