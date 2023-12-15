import sys
from functools import reduce
from typing import List, Tuple


def parse_input(data: str) -> List[Tuple[int, int]]:
    time_line, distance_line = data.splitlines()
    times = time_line.split(":")[1].split()
    distances = distance_line.split(":")[1].split()
    return [(int(times[i]), int(distances[i])) for i in range(len(times))]


def get_race_wins(race: Tuple[int, int]):
    wins = 0
    for x in range(int((race[0] + 1)/2)):
        if (x * (race[0] - x)) > race[1]:
            wins += 2
    
    if (race[0] % 2) == 0:
        wins += 1
    
    return wins


def solve_puzzle(races: List[Tuple[int, int]]):
    result1 = reduce(lambda a, b: a * b, [get_race_wins(r) for r in races], 1)
    print("Part one answer:", result1)

    result2 = get_race_wins((
        int("".join([str(r[0]) for r in races])), 
        int("".join([str(r[1]) for r in races]))
    ))
    print("Part two answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(parse_input(puzzle_input))
