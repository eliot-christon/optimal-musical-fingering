"""
This is the test suite for the build_position_graph function of the musical arrangements.
"""

from backend.src.instruments.neck_instrument import Guitar
from backend.src.music_piece.arrangement.build_position_graph import build_position_graph
from backend.src.music_piece.arrangement.dijkstra import dijkstra
from backend.src.music_piece.music_piece import MusicPiece
from backend.src.music_piece.timed_chord import TimedChord

test_piece = MusicPiece()
test_piece.add_timed_chord(TimedChord(chord=(48, 52, 55), start_time=0.0, duration=1.0))  # C major
test_piece.add_timed_chord(TimedChord(chord=(47, 52, 55), start_time=1.0, duration=1.0))  # E minor
test_piece.add_timed_chord(TimedChord(chord=(52, 57, 61), start_time=3.0, duration=0.8))  # A major


def test_build_position_graph() -> None:
    """Test that the position graph is built correctly."""
    guitar = Guitar()
    graph = build_position_graph(test_piece, guitar)

    # Check that nodes are created
    assert len(graph.nodes) >= len(test_piece.timed_chords)

    # Check that edges are created
    total_edges = sum(len(node.edges) for node in graph.nodes.values())
    assert total_edges > 0

    # Check that all nodes correspond to valid positions
    for node_id, node in graph.nodes.items():
        assert isinstance(node_id, int)
        assert isinstance(node.cost, float)
        for edge in node.edges:
            assert isinstance(edge.to_node.id, int)
            assert isinstance(edge.cost, float)

    # Check the number of edges
    valid_positions = []
    for timed_chord in test_piece.timed_chords:
        notes = list(timed_chord.chord)
        possible_positions = guitar.possible_positions(notes)
        valid_positions.append(
            len([pos for pos in possible_positions if guitar.is_valid_position(pos)])
        )
    expected_edges = valid_positions[0] + valid_positions[-1]  # edges from start and to terminal
    print(valid_positions)
    for i in range(len(valid_positions) - 1):
        expected_edges += valid_positions[i] * valid_positions[i + 1]
    assert total_edges == expected_edges


def test_dijkstra_on_position_graph() -> None:
    """Test that Dijkstra's algorithm works on the position graph."""
    guitar = Guitar()
    graph = build_position_graph(test_piece, guitar)

    # Run Dijkstra's algorithm from the first node
    start_node_id = -1
    result = dijkstra(graph, start_node_id)

    # Check that distances are computed
    assert start_node_id in result.distances
    for node_id in graph.nodes:
        assert node_id in result.distances
        assert isinstance(result.distances[node_id], float)

    # Check that paths are computed
    for node_id in graph.nodes:
        path = result.get_path(node_id)
        assert isinstance(path, list)
        if node_id == start_node_id:
            assert path == [start_node_id]
        elif result.distances[node_id] < float("inf"):
            assert path[0] == start_node_id
            assert path[-1] == node_id

    assert result.get_path(-2) == [
        -1,
        300040235034,
        300050224023,
        402130212021,
        -2,
    ]  # terminal node
