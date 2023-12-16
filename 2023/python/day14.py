import sys
import numpy as np
from functools import cache


def to_array(data: str) -> np.ndarray:
    len_arr = len(data.splitlines())
    return np.array([char for char in data if char != "\n"]).reshape((len_arr, len_arr))


def array_to_str(arr: np.ndarray) -> str:
    return "\n".join(["".join(row) for row in arr])


@cache
def shift_rocks(rock_map: str) -> str:
    col_map = to_array(rock_map).transpose()
    for i, col in enumerate(col_map):
        shifts = 0
        for j, char in enumerate(col):
            if char == ".":
                shifts += 1
            elif char == "#":
                shifts = 0
            elif char == "O":
                col_map[i][j] = "."
                col_map[i][j - shifts] = "O"
    return array_to_str(col_map.transpose())


def get_force(rock_arr: np.ndarray) -> int:
    return sum(
        [(len(row) - i) for i, row in enumerate(rock_arr) for c in row if c == "O" ]
    )


@cache
def get_cycle_force(original_map: str) -> (str, int):
    rock_arr = to_array(original_map)
    # Rotate and shift rocks for North, West, South, East
    for i in range(4):
        rock_arr = np.rot90(rock_arr, 3) if i != 0 else rock_arr
        rock_arr = to_array(shift_rocks(array_to_str(rock_arr)))
    # Reset back to North
    rock_arr = np.rot90(rock_arr, 3)
    
    return array_to_str(rock_arr), get_force(rock_arr)
    

def solve_puzzle(raw_data: str):
    result1 = get_force(to_array(shift_rocks(raw_data)))
    
    print("Part 1 answer:", result1)

    result2 = 0
    rock_map = raw_data
    for _ in range(1_000_000_000):
        rock_map, result2 = get_cycle_force(rock_map)

    print("Part 2 answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)


