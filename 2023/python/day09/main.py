import sys
from functools import reduce
    

def solve_puzzle(puzzle_input: str):
    total = 0
    total2 = 0
    for line in puzzle_input.splitlines():
        # The original sequence
        seq = [int(n) for n in line.split()]
        # For part 1 start with the last number
        total += seq[-1]
        # Part two needs the first in all sequences
        part2_seq = [seq[0]]
        # Keep reducing until we're left with all zeros
        while set(seq) != {0}:
            # Next sequence is made up of deltas
            seq = [seq[i+1] - n for i, n in enumerate(seq[:-1])]
            # For part 1, it's enough to add the last number
            total += seq[-1]
            # Add the first number to the part 2 sequence
            part2_seq.append(seq[0])
        
        # Reduce the part 2 sequence to a single number
        total2 += reduce(lambda x, y: y - x, part2_seq[::-1][1:], 0)
        

    print("Part one answer:", total)
    print("Part two answer:", total2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)