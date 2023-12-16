import sys
from functools import cache, reduce
from typing import List, Tuple


def parse_input(data: str) -> List[Tuple[str, Tuple[int]]]:
    return [
        (line.split(" ")[0], tuple(int(count) for count in line.split(" ")[1].split(",")))
        for line in data.splitlines()
    ]


def handle_dot(springs: str, counts: List[int]):
    return get_combo(springs[1:], counts)


def handle_hash(springs: str, counts: List[int]):
    next_count = counts[0]

    # If we can't replace count of broken springs, exit
    if not set(springs[:next_count]).issubset({"?", "#"}):
        return 0

    # If the spring map finishes here
    if next_count == len(springs):
        # If there are no more counts, we're done
        return 1 if len(counts) == 1 else 0

    # Otherwise, we need a . or ? after the broken springs
    if springs[next_count] in [".", "?"]:
        return get_combo(springs[next_count + 1 :], counts[1:])

    return 0


@cache
def get_combo(springs: str, counts: Tuple[int]) -> int:
    # Exit 1: All broken springs identified
    if not counts:
        # Invalid combo if there are springs left in the map
        return 0 if "#" in springs else 1

    # Exit 2: No more springs to evaluate
    if not springs:
        return 0

    # Exit 3: Not enough chars for remaining counts
    if len(springs) < sum(counts) + len(counts) - 1:
        return 0

    next_spring = springs[0]

    if next_spring == ".":
        return handle_dot(springs, counts)

    if next_spring == "#":
        return handle_hash(springs, counts)

    if next_spring == "?":
        return handle_dot(springs, counts) + handle_hash(springs, counts)


def solve_puzzle(lines: List[Tuple[str, Tuple[int]]]):
    result1 = sum([get_combo(springs, counts) for springs, counts in lines])
    print("Part one answer:", result1)

    result2 = reduce(
        lambda a, b: a + b,
        [get_combo("?".join([springs] * 5), counts * 5) for springs, counts in lines],
        0,
    )
    print("Part two answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(parse_input(puzzle_input))
