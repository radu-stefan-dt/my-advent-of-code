import sys
from typing import List, Tuple, Dict


class Graph(object):
    def __init__(
        self,
        init_graph: Dict[Tuple[int, int], Dict[Tuple[int, int], int]],
    ):
        self.nodes = list(init_graph.keys())
        self.graph = self.build_graph(self.nodes, init_graph)

    def build_graph(self, nodes: List[int], init_graph: List[List[int]]) -> dict:
        # Initialize nodes and neighbors in graph
        graph = {node: {} for node in nodes}
        graph.update(init_graph)

        # Ensure graph is symmetrical
        for node, edges in init_graph.items():
            for neighbor, value in edges.items():
                if not graph[neighbor].get(node):
                    graph[neighbor][node] = value

        return graph

    def get_nodes(self) -> List[int]:
        return self.nodes

    def get_node_neighbors(self, node: Tuple[int, int]) -> List[Tuple[int, int]]:
        return [n for n in self.nodes if self.graph[node].get(n)]

    def value(self, node1: Tuple[int, int], node2: Tuple[int, int]) -> int:
        return int(self.graph[node1][node2])


def parse_input(puzzle_input: str) -> Graph:
    init_graph = {}
    distances = [list(line) for line in puzzle_input.splitlines()]
    for i, line in enumerate(distances):
        for j in range(len(line)):
            init_graph[(i, j)] = {}
            if j - 1 >= 0:
                init_graph[(i, j)][(i, j - 1)] = distances[i][j - 1]
            if j + 1 < len(line):
                init_graph[(i, j)][(i, j + 1)] = distances[i][j + 1]
            if i - 1 >= 0:
                init_graph[(i, j)][(i - 1, j)] = distances[i - 1][j]
            if i + 1 < len(distances):
                init_graph[(i, j)][(i + 1, j)] = distances[i + 1][j]
    return Graph(init_graph)


def is_possible(
    n1: Tuple[int, int],
    n2: Tuple[int, int],
    prev_nodes: Dict[Tuple[int, int], Tuple[int, int]],
) -> bool:
    n3 = prev_nodes.get(n2)
    n4 = prev_nodes.get(n3)

    # Allow the first 3 moves
    if n1 == (0,0) or n2 == (0,0) or n3 is None or n4 is None:
        return True
    
    # Afterwards check if we moved in a line
    if abs(n1[0] - n2[0]) == 1 and abs(n2[0] - n3[0]) == 1 and abs(n3[0] - n4[0]) == 1:
        return False
    if abs(n1[1] - n2[1]) == 1 and abs(n2[1] - n3[1]) == 1 and abs(n3[1] - n4[1]) == 1:
        return False


def dijkstra(
    graph: Graph, source: Tuple[int, int]
) -> Tuple[Dict[Tuple[int, int], Tuple[int, int]], Dict[Tuple[int, int], int]]:
    not_visited = graph.get_nodes()
    previous_nodes = {}
    shortest_path = {node: sys.maxsize if node != source else 0 for node in not_visited}
    while not_visited:
        current_min = None
        # Update current closest node
        for node in not_visited:
            if current_min is None or shortest_path[node] < shortest_path[current_min]:
                current_min = node
        # Evaluate neighbors
        neighbors = graph.get_node_neighbors(current_min)
        for neighbor in neighbors:
            if current_min == (3, 2) and neighbor == (4, 2):
                print("Bang in the middle")
            temp_value = shortest_path[current_min] + graph.value(current_min, neighbor)
            # Check we haven't moved too long in one direction
            if (
                temp_value < shortest_path[neighbor] and
                is_possible(neighbor, current_min, previous_nodes)
            ):
                shortest_path[neighbor] = temp_value
                previous_nodes[neighbor] = current_min
        not_visited.remove(current_min)

    return previous_nodes, shortest_path


def print_out(prev_nodes, shortest_path, start, end):
    path = []
    node = end
    while node != start:
        path.append(node)
        node = prev_nodes[node]
    path.append(start)
    print("Shortest path len is", shortest_path[end])
    print("Path:", " -> ".join(str(n) for n in path[::-1]))


def solve_puzzle(puzzle_input: str) -> int:
    graph = parse_input(puzzle_input)
    previous_nodes, shortest_path = dijkstra(graph, (0, 0))
    print_out(previous_nodes, shortest_path, (0, 0), (4, 4))


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
