import sys
from typing import Tuple, Dict
from collections import Counter
from functools import reduce


def parse_input(puzzle_input: str) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    lines = puzzle_input.splitlines()
    instructions = lines[0]
    nodes = {}
    for line in lines[1:]:
        if line:
            name, neighbors = line.split(" = ")
            left, right = neighbors.split(", ")
            nodes[name] = (left[1:], right[:-1])

    return instructions, nodes


def prime_factors(n):
    factors = []
    divisor = 2

    # Shrink down n by dividing
    while n > 1:
        # Division must be exact
        while n % divisor == 0:
            # Keep on adding as long as you can divide
            factors.append(divisor)
            n //= divisor 
        divisor += 1

    return factors


def part_one(instructions: str, nodes: Dict[str, Tuple[str, str]]):
    next_node = "AAA"
    index = 0
    steps = 0
    while next_node != "ZZZ":
        direction = instructions[index]
        next_node = nodes[next_node][0 if direction == "L" else 1]
        # Handle index with wrap around
        index = (index + 1) % len(instructions)
        steps += 1

    print("Part one answer:", steps)


def find_path_length(
    instructions: str, start: str, nodes: Dict[str, Tuple[str, str]]
) -> int:
    next_node = start
    index = 0
    steps = 0
    while not next_node.endswith("Z"):
        direction = instructions[index]
        next_node = nodes[next_node][0 if direction == "L" else 1]
        # Handle index with wrap around
        index = (index + 1) % len(instructions)
        steps += 1

    return steps


def part_two(instructions: str, nodes: Dict[str, Tuple[str, str]]):
    next_nodes = set([name for name in nodes.keys() if name.endswith("A")])

    factorization = dict()
    for node in next_nodes:
        factorization.update(
            Counter(prime_factors(find_path_length(instructions, node, nodes)))
        )

    result = reduce(lambda x, y: x * y, [k**v for k, v in factorization.items()], 1)
    print("Part two answer:", result)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    part_one(*parse_input(puzzle_input))
    part_two(*parse_input(puzzle_input))
