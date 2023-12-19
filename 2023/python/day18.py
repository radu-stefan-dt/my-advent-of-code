import re
import sys
from typing import List, Tuple


def parse_part_one(puzzle_input: str) -> List[Tuple[str, int]]:
    return [(l.split()[0], int(l.split()[1])) for l in puzzle_input.splitlines()]


def parse_part_two(puzzle_input: str) -> List[Tuple[str, int]]:
    nodes = []
    for l in puzzle_input.splitlines():
        code = re.search(r'\(#(.*?)\)', l).group(1)
        nodes.append(("RDLU"[int(code[-1])], int(code[:-1], 16)))
    return nodes


def area(nodes: List[Tuple[int, int]], border_correction: int) -> int:
    i_max = len(nodes) - 1
    computed = sum([nodes[i][0] * nodes[i+1][1] - nodes[i+1][0] * nodes[i][1] for i in range(i_max)])
    return int(abs(computed)/2 + border_correction)


def calculate_area(steps: List[Tuple[str, int]]) -> int:
    nodes = [(0, 0)]
    perimeter = 0
    while steps:
        direction, count = steps.pop(0)
        # Use R, U for half of the perimeter
        perimeter += count if direction in "RU" else 0
        last_node = nodes[-1]
        next_node = (
            last_node[0] + (count if direction == "D" else -count if direction == "U" else 0),
            last_node[1] + (count if direction == "R" else -count if direction == "L" else 0)
        )
        nodes.append(next_node)
    return area(nodes, perimeter + 1)


def solve_puzzle(puzzle_input: str):
    result = calculate_area(parse_part_one(puzzle_input))
    print("Part one answer:", result)

    result2 = calculate_area(parse_part_two(puzzle_input))
    print("Part two answer:", result2)
    

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
