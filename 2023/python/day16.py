import sys
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Tuple


CELL_CACHE: Dict[Tuple[int, int], List[str]] = {}


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


def save_cell(position: Tuple[int, int], direction: str) -> bool:
    if position in CELL_CACHE:
        if direction in CELL_CACHE[position]:
            raise Exception("Loop detected")
        else:
            CELL_CACHE[position].append(direction)
            return 0
    else:
        CELL_CACHE[position] = [direction]
        return 1


def follow_path(
    raw_map: str, start: Tuple[int, int] = None, direction: str = "right"
) -> int:
    try:
        path_score = 0
        path_score += save_cell(start, direction) if start else 0
        
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
            return path_score

        # Option 2: Continue on path
        if (
            next_cell == "." or
            (next_cell == "|" and direction in ["up", "down"]) or
            (next_cell == "-" and direction in ["left", "right"])
            ):
            path_score += save_cell(next_coords, direction)
            if direction in ["right", "left"]:
                j = next_coords[1] + (1 if direction == "right" else -1)
                while j < len(grid[0]) and j >= 0:
                    if grid[next_coords[0]][j] in [".", "-"]:
                        path_score += save_cell((next_coords[0], j), direction)
                    else:
                        next_coords = (next_coords[0], j)
                        next_cell = grid[next_coords[0]][next_coords[1]]
                        break
                    j += 1 if direction == "right" else -1
            elif direction in ["up", "down"]:
                i = next_coords[0] + (1 if direction == "down" else -1)
                while i < len(grid) and i >= 0:
                    if grid[i][next_coords[1]] in [".", "|"]:
                        path_score += save_cell((i, next_coords[1]), direction)
                    else:
                        next_coords = (i, next_coords[1])
                        next_cell = grid[next_coords[0]][next_coords[1]]
                        break
                    i += 1 if direction == "down" else -1

        # Option 3: Change direction based on mirror
        if next_cell in ["\\", "/"]:
            return (
                path_score +
                follow_path(raw_map, next_coords, mirror_direction(next_cell, direction))
            )
        # Option 4: Split path up and down
        elif next_cell == "|":
            return (
                path_score +
                follow_path(raw_map, next_coords, "up") +
                follow_path(raw_map, next_coords, "down")
            )
        # Option 5: Split path left and right
        elif next_cell == "-":
            return (
                path_score + 
                follow_path(raw_map, next_coords, "left") +
                follow_path(raw_map, next_coords, "right")
            )
        else:
            return path_score
    except:
        return path_score


def follow_paths(batch: List[Tuple[Tuple[int, int], str, str]]) -> int:
    score = -1
    for start, direction, data in batch:
        CELL_CACHE.clear()
        score = max([follow_path(data, start, direction), score])
    return score


def solve_puzzle(data: str):
    result1 = follow_path(data, direction="right")
    print("Part one answer:", result1)

    grid = to_grid(data)
    starts = (
        [((0, x), "down", data) for x in range(len(grid[0]))] + 
        [((len(grid) - 1, x), "up", data) for x in range(len(grid[0]))] +
        [((x, 0), "right", data) for x in range(len(grid))] + 
        [((x, len(grid[0]) - 1), "left", data) for x in range(len(grid))]
    )
    batches = [starts[i::32] for i in range(32)]

    with ProcessPoolExecutor(max_workers=32) as executor:
        result2 = max(executor.map(follow_paths, batches))
        print("Part two answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
