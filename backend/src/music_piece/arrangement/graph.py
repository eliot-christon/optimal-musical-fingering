"""
This module forms the generic graph structure for arranging musical pieces.
Supports both node and edge costs.
"""


class Edge:
    """Represents a directed edge between two nodes with an associated cost."""

    def __init__(self, to_node: "Node", cost: float = 0.0) -> None:
        """Initializes an Edge with a destination node and a cost."""
        self.to_node = to_node
        self.cost = cost

    def __repr__(self) -> str:
        """Returns a string representation of the edge."""
        return f"Edge(to_node={self.to_node.id}, cost={self.cost})"


class Node:
    """Class representing a node in the arrangement graph.
    Each node corresponds to a specific musical position or state.
    Node has a cost, and outgoing edges with their own costs."""

    def __init__(self, node_id: int, cost: float = 0.0) -> None:
        """Initializes a Node with a unique ID and an associated cost."""
        self.id = node_id
        self.cost = cost
        self.edges: list[Edge] = []

    def __repr__(self) -> str:
        """Returns a string representation of the node."""
        return f"Node(id={self.id}, cost={self.cost}, edges={len(self.edges)})"

    def add_edge(self, to_node: "Node", edge_cost: float = 0.0) -> None:
        """Adds a directed edge to another node with a specified cost."""
        self.edges.append(Edge(to_node, edge_cost))


class Graph:
    """Manages a collection of nodes and edges for the arrangement graph."""

    def __init__(self) -> None:
        """Initializes an empty graph."""
        self.nodes: dict[int, Node] = {}

    def __repr__(self) -> str:
        """Returns a string representation of the graph."""
        return f"Graph(nodes={list(self.nodes.keys())})"

    def add_node(self, position_id: int, cost: float = 0.0) -> Node:
        """Adds a node to the graph and returns it."""
        node = Node(position_id, cost)
        self.nodes[position_id] = node
        return node

    def add_edge(self, from_id: int, to_id: int, edge_cost: float = 0.0) -> None:
        """Adds an edge between two nodes by their position IDs."""
        from_node = self.nodes.get(from_id)
        to_node = self.nodes.get(to_id)
        if from_node and to_node:
            from_node.add_edge(to_node, edge_cost)
