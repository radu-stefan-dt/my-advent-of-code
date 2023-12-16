import re
import sys


def get_code(line: str):
    subs ={
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }

    first_match, last_match = None, None

    expr = r'[1-9]|one|two|three|four|five|six|seven|eight|nine'
    first_match = re.search(expr, line)

    for i in range(0, len(line)):
        last_match = re.search(expr, line[len(line)-1-i:])
        if last_match is not None:
            break

    if first_match is None and last_match is None:
        return 0
    
    first_digit = subs[first_match.group()] if first_match.group() in subs else first_match.group()
    last_digit = subs[last_match.group()] if last_match.group() in subs else last_match.group()
    
    return int(first_digit + last_digit)


def get_calibration_code(line: str):
    digits = [d for d in line if d.isdigit()]

    if len(digits) == 0:
        return 0

    return int(digits[0] + digits[-1])


def solve_puzzle(data: str):
    result1 = sum(get_calibration_code(line) for line in data.splitlines())
    print("Part one answer:", result1)

    result2 = sum(get_code(line) for line in data.splitlines())
    print("Part two answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)