"""
Dijkstra's algorithm for finding the shortest path in a graph with node and edge costs.
"""

import heapq

from .graph import Graph


class DijkstraResult:
    """
    Holds the results of Dijkstra's algorithm, including distances and previous nodes.
    """

    def __init__(self, distances: dict[int, float], previous: dict[int, int | None]) -> None:
        """Initializes the DijkstraResult with distances and previous nodes."""
        self.distances = distances
        self.previous = previous

    def __repr__(self) -> str:
        """Returns a string representation of the DijkstraResult."""
        return f"DijkstraResult(distances={self.distances}, previous={self.previous})"

    def get_path(self, target_id: int | None) -> list[int]:
        """Reconstructs the shortest path to the target node."""
        path = []
        current = target_id
        while current is not None:
            path.append(current)
            current = self.previous.get(current)
        return path[::-1]


def dijkstra(graph: Graph, start_id: int) -> DijkstraResult:
    """Implements Dijkstra's algorithm to find the shortest paths
    from the start node to all other nodes in the graph."""
    distances: dict[int, float] = {node_id: float("inf") for node_id in graph.nodes}
    previous: dict[int, int | None] = dict.fromkeys(graph.nodes)
    distances[start_id] = graph.nodes[start_id].cost
    queue: list[tuple[float, int]] = [(distances[start_id], start_id)]

    while queue:
        current_dist, current_id = heapq.heappop(queue)
        current_node = graph.nodes[current_id]
        for edge in current_node.edges:
            neighbor_id = edge.to_node.id
            new_dist = current_dist + edge.cost + edge.to_node.cost
            if new_dist < distances[neighbor_id]:
                distances[neighbor_id] = new_dist
                previous[neighbor_id] = current_id
                heapq.heappush(queue, (new_dist, neighbor_id))
    return DijkstraResult(distances, previous)
