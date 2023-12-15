import re
import sys
from typing import List


def part_one(schematic: List[List[str]]):
    total = 0
    number_length = 0
    for i, row in enumerate(schematic):
        for j, col in enumerate(row):
            # If number was found, skip past the number
            if number_length > 1:
                number_length -= 1
                continue
            # If digit found, check how long number is
            if col.isdigit():
                number_length = 0
                for k in range(j, len(row)):
                    if row[k].isdigit():
                        number_length += 1
                    else:
                        break
                number = int(''.join(row[j:j+number_length]))
                is_valid = False
                # Then check surroundings for symbols
                # Check Left
                if j-1 >= 0 and schematic[i][j-1] != '.':
                    is_valid = True
                # Above
                if i-1 >= 0:
                    min_right = j-1 if j-1 >= 0 else j
                    max_right = j+number_length if j+number_length < len(row) else j+number_length-1
                    for k in range(min_right, max_right+1):
                        if schematic[i-1][k] != '.':
                            is_valid = True
                            break
                # Right
                if j + number_length < len(row) and schematic[i][j+number_length] != '.':
                    is_valid = True
                # Below
                if i+1 < len(schematic):
                    min_right = j-1 if j-1 >= 0 else 0
                    max_right = j+number_length if j+number_length < len(row) else j+number_length-1
                    for k in range(min_right, max_right+1):
                        if schematic[i+1][k] != '.':
                            is_valid = True
                            break

                if is_valid:
                    total += number
    
    print("Part one answer:", total)


def part_two(schematic: List[List[str]]):
    total = 0
    for i, row in enumerate(schematic):
        for j, col in enumerate(row):
            # If we found asterisk, check if it's valid
            if col == '*':
                adjacent_numbers = []
                # Check left
                left_match = re.search(r"\d+$", "".join(row[:j]))
                if left_match:
                    adjacent_numbers.append(int(left_match.group(0)))
                # Check right
                right_match = re.search(r"^\d+", "".join(row[j+1:]))
                if right_match:
                    adjacent_numbers.append(int(right_match.group(0)))
                # Check above
                if i-1 >= 0:
                    above_matches = re.finditer(r"\d+", ''.join(schematic[i-1]))
                    for match in above_matches:
                        if match.start() <= j + 1 and match.end() >= j:
                            adjacent_numbers.append(int(match.group(0)))
                # Check below
                if i + 1 < len(schematic):
                    below_matches = re.finditer(r"\d+", ''.join(schematic[i+1]))
                    for match in below_matches:
                        if match.start() <= j + 1 and match.end() >= j:
                            adjacent_numbers.append(int(match.group(0)))
                # If at exactly 2 numbers found, it's valid
                if len(adjacent_numbers) == 2:
                    total += adjacent_numbers[0] * adjacent_numbers[1]
    
    print("Part two answer:", total)


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        puzzle_input = f.read()
    schematic = [list(row) for row in puzzle_input.splitlines()]

    part_one(schematic)
    part_two(schematic)