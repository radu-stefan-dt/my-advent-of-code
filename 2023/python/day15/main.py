import re
from functools import cache, reduce
from typing import List, Tuple


def get_puzzle_input() -> str:
    with open("day15/input.txt") as f:
        return f.read()


@cache
def hash(data: str) -> int:
    return reduce(lambda x, y: ((x + ord(y)) * 17) % 256, data, 0)


def find_slot(box: List[Tuple[str, int]], label: str) -> int:
    for slot, lens in enumerate(box):
        if lens[0] == label:
            return slot
    return -1


def score(i: int, box: List[Tuple[str, int]]) -> int:
    return sum([i * j * int(lens[1]) for j, lens in enumerate(box, 1)])


def solve_puzzle():
    data = get_puzzle_input()

    result1 = sum([hash(step) for step in data.splitlines()[0].split(",")])
    print("Part one answer:", result1)

    boxes = [[] for _ in range(256)]
    for step in data.splitlines()[0].split(","):
        label, op, fl = re.match(r'^(.+?)(=|-)(.*?)$', step).groups()
        box_i = hash(label)
        slot = find_slot(boxes[box_i], label)
        # Add
        if op == "=":
            # if lens of label exists, update fl
            if slot >= 0:
                boxes[box_i][slot][1] = fl
            # else append new lens
            else:
                boxes[box_i].append([label, fl])
        # Remove
        else:
            if slot >= 0:
                boxes[box_i].pop(slot)
    
    result2 = sum([score(i, box) for i, box in enumerate(boxes, 1)])
    print("Part two answer: ", result2)


if __name__ == "__main__":
    solve_puzzle()