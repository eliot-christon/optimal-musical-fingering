"""
This module provides the bulding of a position graph for arranging musical pieces.
"""

from backend.src.instruments.neck_instrument import NeckInstrument
from backend.src.music_piece.arrangement.graph import Graph
from backend.src.music_piece.music_piece import MusicPiece
from backend.src.positions.neck_position import NeckPosition
from backend.src.utils.num2note import num2note


def build_position_graph(music_piece: MusicPiece, instrument: NeckInstrument) -> tuple[Graph, str]:
    """
    Builds a graph of positions for the given music piece and instrument.

    Parameters:
        music_piece (MusicPiece): The music piece to build the graph for.
        instrument (NeckInstrument): The instrument to use for building the graph.

    Returns:
        tuple[Graph, str]: A tuple containing the position graph and any error messages.
    """
    graph = Graph()
    position_map: list[list[int]] = []
    errors: list[str] = []

    for time_index, timed_chord in enumerate(music_piece.timed_chords):
        position_map.append([])
        notes = list(timed_chord.chord)
        valid_positions = [
            pos for pos in instrument.possible_positions(notes) if instrument.is_valid_position(pos)
        ]

        if len(valid_positions) == 0:
            notes_str = ", ".join([num2note(note) for note in notes])
            errors.append(f"No valid positions found for notes: {notes_str} for {instrument}")
            continue

        for pos in valid_positions:
            position_id = pos.to_placement_code() * 1000 + time_index  # unique ID
            graph.add_node(position_id, cost=instrument.position_cost(pos, check_valid=False))
            position_map[time_index].append(position_id)

        if time_index > 0:
            for prev_id in position_map[time_index - 1]:
                for curr_id in position_map[time_index]:
                    transition_cost = instrument.transition_cost(
                        NeckPosition.from_placement_code(prev_id // 1000),
                        NeckPosition.from_placement_code(curr_id // 1000),
                    )
                    graph.add_edge(prev_id, curr_id, edge_cost=transition_cost)

    # add a start node that connects to all first positions with 0 cost
    # add a terminal node that all last positions connect to with 0 cost
    start_node_id = -1
    terminal_node_id = -2
    graph.add_node(start_node_id, cost=0.0)
    graph.add_node(terminal_node_id, cost=0.0)

    for first_id in position_map[0]:
        graph.add_edge(start_node_id, first_id, edge_cost=0.0)
    for last_id in position_map[-1]:
        graph.add_edge(last_id, terminal_node_id, edge_cost=0.0)

    return graph, "\n".join(errors)
