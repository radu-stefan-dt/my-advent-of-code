import sys
import numpy as np
from typing import List


def get_maps(data: str) -> List[np.ndarray]:
    arrs = []
    for entry in data.split("\n\n"):
        lines = entry.splitlines()
        arrs.append(np.array([char for char in entry if char != "\n"]).reshape((len(lines), len(lines[0]))))
    return arrs


def check_symmetry(map_arr: np.ndarray, i: int, smudges: int = 0) -> int:
    # Check inwards for full reflection
    for j in range(0, i):
        # Reflected rows that fall outside are OK
        if 2 * i + 1 - j >= len(map_arr):
            continue
        other_row = "".join(map_arr[j])
        mirror_row = "".join(map_arr[2 * i + 1 - j])
        row_diff = sum([1 for k, a in enumerate(other_row) if mirror_row[k] != a])
        # Smudges apply exactly to the whole pattern
        smudges -= row_diff
        if smudges < 0:
            break

    return i + 1 if smudges == 0 else 0


def find_reflection(map_arr: np.ndarray, smudges: int = 0) -> int:
    # Go through each row
    for i in range(len(map_arr) - 1):
        this_row = "".join(map_arr[i])
        next_row = "".join(map_arr[i + 1])

        # Check reflection accounting for smudges
        row_diff = sum([1 for k, a in enumerate(this_row) if next_row[k] != a])
        if row_diff <= smudges:
            ref_idx = check_symmetry(map_arr, i, smudges - row_diff)
            if ref_idx > 0:
                return ref_idx
    return 0


def solve_puzzle(puzzle_input: str):
    maps = get_maps(puzzle_input)
    result1 = (
        sum([find_reflection(map_arr.transpose(), 0) for map_arr in maps]) +
        sum([100 * find_reflection(map_arr, 0) for map_arr in maps])
    )
    result2 = (
        sum([find_reflection(map_arr.transpose(), 1) for map_arr in maps]) + 
        sum([100 * find_reflection(map_arr, 1) for map_arr in maps])
    )

    print("Part 1 answer:", result1)
    print("Part 2 answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
