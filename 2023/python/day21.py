import sys
from typing import Tuple, List


def parse_input(puzzle_input: str) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
    grid = []
    for i, row in enumerate(puzzle_input.splitlines()):
        grid.append(list(row))
        if "S" in row:
            start = (i, row.index("S"))
    return start, grid


def get_neighbors(
    indexed_point: Tuple[int, Tuple[int, int]],
    grid: List[Tuple[int, int]],
    infinite_map: bool,
) -> List[Tuple[int, int]]:
    (i, j), (x, y) = indexed_point
    neighbors = []
    if (x - 1 >= 0 or infinite_map) and grid[x - 1][y] != "#":
        if x - 1 < 0:
            neighbors.append(((i - 1, j), (len(grid) - 1, y)))
        else:
            neighbors.append(((i, j), (x - 1, y)))
    if (y - 1 >= 0 or infinite_map) and grid[x][y - 1] != "#":
        if y - 1 < 0:
            neighbors.append(((i, j - 1), (x, len(grid[0]) - 1)))
        else:
            neighbors.append(((i, j), (x, y - 1)))
    if x + 1 >= len(grid) and infinite_map:
        if grid[(x + 1) % len(grid)][y] != "#":
            neighbors.append(((i + 1, j), ((x + 1) % len(grid), y)))
    if x + 1 < len(grid):
        if grid[x + 1][y] != "#":
            neighbors.append(((i, j), (x + 1, y)))
    if y + 1 >= len(grid[0]) and infinite_map:
        if grid[x][(y + 1) % len(grid[0])] != "#":
            neighbors.append(((i, j + 1), (x, (y + 1) % len(grid[0]))))
    if y + 1 < len(grid[0]) and grid[x][y + 1] != "#":
        neighbors.append(((i, j), (x, y + 1)))

    return neighbors


def part_one(puzzle_input: str) -> int:
    start, grid = parse_input(puzzle_input)
    starts = [((0, 0), start)]
    for _ in range(64):
        new_locations = [get_neighbors(ip, grid, False) for ip in starts]
        starts = list(set([point for points in new_locations for point in points]))
    print("Part one answer:", len(starts))

    starts = [((0, 0), start)]
    for _ in range(26501365):
        new_locations = [get_neighbors(ip, grid, True) for ip in starts]
        starts = list(set([ip for points in new_locations for ip in points]))
    print("Part two answer:", len(starts))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    part_one(puzzle_input)
