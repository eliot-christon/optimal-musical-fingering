"""
This module provides functionality for arranging musical pieces.
The idea is to create a playable arrangement of a music piece
based on the positions available for a given neck instrument.
"""

from backend.src.instruments.neck_instrument import NeckInstrument
from backend.src.music_piece.arrangement.build_position_graph import build_position_graph
from backend.src.music_piece.arrangement.dijkstra import dijkstra
from backend.src.music_piece.music_piece import MusicPiece
from backend.src.positions.neck_position import NeckPosition


def neck_arrangement(music_piece: MusicPiece, instrument: NeckInstrument) -> list[NeckPosition]:
    """Arranges the music piece for the specified instrument.
    Taking into account:
        - position cost
        - transition cost
    """
    graph, errors = build_position_graph(music_piece, instrument)
    if len(graph.nodes) == 0:
        msg = "No valid positions found for the entire piece."
        raise ValueError(msg)
    if errors:
        raise ValueError(
            "Errors found during neck arrangement:\n" + "\n\t".join(errors.split("\n"))
        )

    start_node_id = -1
    terminal_node_id = -2
    result = dijkstra(graph, start_node_id)
    if terminal_node_id not in result.distances or result.distances[terminal_node_id] == float(
        "inf"
    ):
        msg = "No valid arrangement found from start to end."
        raise ValueError(msg)

    path_ids = result.get_path(terminal_node_id)
    return [
        NeckPosition.from_placement_code(node_id // 1000)  # last three digits are time index
        for node_id in path_ids
        if node_id not in (start_node_id, terminal_node_id)
    ]
