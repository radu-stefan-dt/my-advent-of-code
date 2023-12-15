import sys
from typing import List, Tuple
from functools import reduce


def parse_input(data: str, exp_factor: int) -> List[Tuple[int, int]]:
    # Create a 2D array of the input
    galaxy_map = [list(line) for line in data.splitlines()]
    # Find rows that have only dots
    exp_rows = [i for i, row in enumerate(galaxy_map) if set(row) == {"."}]
    # Find columns that have only dots
    exp_cols = [
        j
        for j in range(0, len(galaxy_map[0]))
        if set(galaxy_map[i][j] for i in range(0, len(galaxy_map))) == {"."}
    ]
    # Find all galaxies
    return [
        (
            i + len(list(filter(lambda x: x < i, exp_rows))) * (exp_factor - 1),
            j + len(list(filter(lambda x: x < j, exp_cols))) * (exp_factor - 1),
        )
        for i, row in enumerate(galaxy_map)
        for j, char in enumerate(row)
        if char == "#"
    ]


def solve_puzzle(puzzle_input: str, exp_factor: int = 2) -> int:
    galaxies = parse_input(puzzle_input, exp_factor)
    # Go through every galaxy and add up the distance to others
    return reduce(
        lambda a, b: a + b,
        [
            abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
            for i, g1 in enumerate(galaxies[:-1])
            for g2 in galaxies[i + 1 :]
        ],
        0,
    )


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    print("Part one answer:", solve_puzzle(puzzle_input))
    print("Part two answer:", solve_puzzle(puzzle_input, 1_000_000))
