import sys
import numpy as np
from typing import List, Dict, Tuple


CACHE: Dict[Tuple[int, int], List[str]] = {}


def to_grid(data: str) -> np.ndarray:
    size = len(data.splitlines())
    return np.array([list(line) for line in data.splitlines()]).reshape((size, size))


def mirror_direction(mirror: str, direction: str) -> str:
    return {
        "up": "right" if mirror == "/" else "left",
        "right": "up" if mirror == "/" else "down",
        "down": "left" if mirror == "/" else "right",
        "left": "down" if mirror == "/" else "up",
    }[direction]


def cache(position: Tuple[int, int], direction: str) -> bool:
    if position in CACHE:
        if direction in CACHE[position]:
            return True
        else:
            CACHE[position].append(direction)
    else:
        CACHE[position] = [direction]

    return False


def follow_path(
    raw_map: str, start: Tuple[int, int] = None, direction: str = "right"
) -> int:
    if start:
        if cache(start, direction):
            return
    
    # Advance on path
    grid = to_grid(raw_map)
    next_coords = {
        "right": (start[0], start[1] + 1) if start[1] + 1 < len(grid[0]) else None,
        "left": (start[0], start[1] - 1) if start[1] - 1 >= 0 else None,
        "up": (start[0] - 1, start[1]) if start[0] - 1 >= 0 else None,
        "down": (start[0] + 1, start[1]) if start[0] + 1 < len(grid) else None
    }[direction] if start else (0, 0)
    next_cell = grid[next_coords[0]][next_coords[1]] if next_coords else None

    # Option 1: End of path
    if not next_cell:
        return

    # Option 2: Continue on path
    if (
        next_cell == "." or
        (next_cell == "|" and direction in ["up", "down"]) or
        (next_cell == "-" and direction in ["left", "right"])
        ):
        if cache(next_coords, direction):
            return
        if direction in ["right", "left"]:
            j = next_coords[1] + (1 if direction == "right" else -1)
            while j < len(grid[0]) and j >= 0:
                if grid[next_coords[0]][j] in [".", "-"]:
                    if cache((next_coords[0], j), direction):
                        return
                else:
                    next_coords = (next_coords[0], j)
                    next_cell = grid[next_coords[0]][next_coords[1]]
                    break
                j += 1 if direction == "right" else -1
        elif direction in ["up", "down"]:
            i = next_coords[0] + (1 if direction == "down" else -1)
            while i < len(grid) and i >= 0:
                if grid[i][next_coords[1]] in [".", "|"]:
                    if cache((i, next_coords[1]), direction):
                        return
                else:
                    next_coords = (i, next_coords[1])
                    next_cell = grid[next_coords[0]][next_coords[1]]
                    break
                i += 1 if direction == "down" else -1
                
    # Option 3: Change direction based on mirror
    if next_cell in ["\\", "/"]:    
        return follow_path(raw_map, (next_coords[0], next_coords[1]), mirror_direction(next_cell, direction))
    # Option 4: Split path up and down
    elif next_cell == "|":
        return follow_path(raw_map, (next_coords[0], next_coords[1]), "up"), follow_path(raw_map, (next_coords[0], next_coords[1]), "down")
    # Option 5: Split path left and right
    elif next_cell == "-":
        return follow_path(raw_map, (next_coords[0], next_coords[1]), "left"), follow_path(raw_map, (next_coords[0], next_coords[1]), "right")
    


def solve_puzzle(data: str):
    follow_path(data, direction="right")
    print("Part one answer:", len(CACHE))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
