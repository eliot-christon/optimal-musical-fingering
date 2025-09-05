"""
This is the test suite for the dijkstra module of the musical arrangements.
"""

from backend.src.music_piece.arrangement.dijkstra import dijkstra
from backend.src.music_piece.arrangement.graph import Graph

test_graph = Graph()
test_graph.add_node(1, cost=1.0)
test_graph.add_node(2, cost=8.0)
test_graph.add_node(3, cost=2.0)
test_graph.add_node(4, cost=2.8)
test_graph.add_node(6, cost=4.0)
test_graph.add_node(7, cost=0.5)

test_graph.add_edge(1, 3, edge_cost=1.5)
test_graph.add_edge(1, 4, edge_cost=2.5)
test_graph.add_edge(3, 6, edge_cost=2.0)
test_graph.add_edge(4, 6, edge_cost=0.1)
test_graph.add_edge(3, 7, edge_cost=0.5)
test_graph.add_edge(4, 7, edge_cost=1.0)


def test_dijkstra_distances() -> None:
    """Test that dijkstra computes the correct shortest distances."""
    result = dijkstra(test_graph, start_id=1)
    assert result.distances[1] == 1.0  # Start node cost
    assert result.distances[2] == float("inf")  # Unreachable node
    assert result.distances[3] == 1.0 + 1.5 + 2.0  # 1 -> 3
    assert result.distances[4] == 1.0 + 2.5 + 2.8  # 1 -> 4
    assert result.distances[6] == 1.0 + 2.5 + 2.8 + 0.1 + 4.0  # 1 -> 4 -> 6
    assert result.distances[7] == 1.0 + 1.5 + 2.0 + 0.5 + 0.5  # 1 -> 3 -> 7
    assert 8 not in result.distances  # Non-existent node


def test_dijkstra_paths() -> None:
    """Test that dijkstra computes the correct shortest paths."""
    result = dijkstra(test_graph, start_id=1)
    assert result.get_path(1) == [1]
    assert result.get_path(3) == [1, 3]
    assert result.get_path(4) == [1, 4]
    assert result.get_path(6) == [1, 4, 6]
    assert result.get_path(7) == [1, 3, 7]
    assert result.get_path(2) == [2]
    assert result.get_path(8) == [8]  # Non-existent node
