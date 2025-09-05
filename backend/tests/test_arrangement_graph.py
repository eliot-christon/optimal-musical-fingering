"""
This is the test suite for the graph module of the musical arrangements.
"""

from backend.src.music_piece.arrangement.graph import Graph

test_graph = Graph()
node_a = test_graph.add_node(1, cost=1.0)
node_b = test_graph.add_node(2, cost=2.0)
node_c = test_graph.add_node(3, cost=3.0)
node_d = test_graph.add_node(44, cost=4.0)

test_graph.add_edge(1, 2, edge_cost=1.5)
test_graph.add_edge(1, 3, edge_cost=2.5)
test_graph.add_edge(2, 44, edge_cost=1.0)
test_graph.add_edge(3, 44, edge_cost=0.5)


def test_graph_nodes() -> None:
    """Test that nodes are added correctly to the graph."""
    assert len(test_graph.nodes) == 4
    assert test_graph.nodes[1].cost == 1.0
    assert test_graph.nodes[2].cost == 2.0
    assert test_graph.nodes[3].cost == 3.0
    assert test_graph.nodes[44].cost == 4.0


def test_graph_edges() -> None:
    """Test that edges are added correctly between nodes."""
    assert len(test_graph.nodes[1].edges) == 2
    assert test_graph.nodes[1].edges[0].to_node.id == 2
    assert test_graph.nodes[1].edges[0].cost == 1.5
    assert test_graph.nodes[1].edges[1].to_node.id == 3
    assert test_graph.nodes[1].edges[1].cost == 2.5

    assert len(test_graph.nodes[2].edges) == 1
    assert test_graph.nodes[2].edges[0].to_node.id == 44
    assert test_graph.nodes[2].edges[0].cost == 1.0

    assert len(test_graph.nodes[3].edges) == 1
    assert test_graph.nodes[3].edges[0].to_node.id == 44
    assert test_graph.nodes[3].edges[0].cost == 0.5

    assert len(test_graph.nodes[44].edges) == 0
