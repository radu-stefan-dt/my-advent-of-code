import sys
from typing import List, Tuple, Dict, Union, Optional
from matplotlib import path as mpath


def parse_input(data: str) -> Tuple[Tuple[int, int], List[List[str]]]:
    pipe_map = []
    for i, line in enumerate(data.splitlines()):
        pipe_map.append([])
        for j, char in enumerate(line):
            pipe_map[i].append(char)
            if char == "S":
                start = [i, j]

    return start, pipe_map


def opposite(direction: str) -> str:
    return {
        "above": "below",
        "below": "above",
        "left": "right",
        "right": "left",
    }.get(direction)


def get_next_direction(from_direction: str, pipe: str) -> str:
    return {
        "above": "below" if pipe == "|" else "left" if pipe == "J" else "right",
        "below": "above" if pipe == "|" else "left" if pipe == "7" else "right",
        "left": "right" if pipe == "-" else "above" if pipe == "J" else "below",
        "right": "left" if pipe == "-" else "above" if pipe == "L" else "below",
    }.get(from_direction)


def get_first_step(
    start: Tuple[int, int], pipe_map: List[List[str]]
) -> Dict[str, Optional[Union[str, Tuple[int, int]]]]:
    # For any direction, only some pipes are valid
    CONNECTORS = {
        "above": ["|", "7", "F"],
        "below": ["|", "J", "L"],
        "left": ["-", "F", "L"],
        "right": ["-", "J", "7"],
    }

    # Shorthand
    coords = {
        "above": [start[0] - 1, start[1]],
        "below": [start[0] + 1, start[1]],
        "left": [start[0], start[1] - 1],
        "right": [start[0], start[1] + 1],
    }

    # Neighbor pipe evaluation only needed for start point
    next_nodes = [
        {
            "direction": direction,
            "pipe": pipe_map[coords[direction][0]][coords[direction][1]]
            if (
                coords[direction][0] > 0
                and coords[direction][0] < len(pipe_map)
                and coords[direction][1] > 0
                and coords[direction][1] < len(pipe_map[0])
                and pipe_map[coords[direction][0]][coords[direction][1]]
                in CONNECTORS[direction]
            )
            else None,
            "coords": coords[direction],
        }
        for direction in ["above", "below", "left", "right"]
    ]

    # We go in first direction possible
    next_details = next(filter(lambda x: x["pipe"] is not None, next_nodes))
    return next_details


def solve_puzzle(puzzle_input: str):
    start, pipe_map = parse_input(puzzle_input)
    path = []

    # First step details
    next_details = get_first_step(start, pipe_map)
    next_direction = next_details["direction"]
    next_node = next_details["pipe"]
    next_coords = next_details["coords"]
    path.append(next_coords)

    # Keep going until we've reached S again
    while next_node != "S":
        next_direction = get_next_direction(opposite(next_direction), next_node)
        next_coords = {
            "above": [next_coords[0] - 1, next_coords[1]],
            "below": [next_coords[0] + 1, next_coords[1]],
            "left": [next_coords[0], next_coords[1] - 1],
            "right": [next_coords[0], next_coords[1] + 1],
        }.get(next_direction)
        path.append(next_coords)
        next_node = pipe_map[next_coords[0]][next_coords[1]]

    print("Part one answer:", int((len(path) + 1) / 2))

    # Count the points within the maze path
    inner = list(
        mpath.Path(path).contains_points(
            [
                [i, j]
                for i, line in enumerate(pipe_map)
                for j, _ in enumerate(line)
                if [i, j] not in path
            ]
        )
    ).count(True)

    print("Part two answer:", inner)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
