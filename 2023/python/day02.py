import re
import sys


def part_one(data: str):
    max_counts = { 'red': 12, 'green': 13, 'blue': 14 }
    total = 0
    expr = r'(\d+) (blue|red|green)'

    for line in data.splitlines():
        possible = True
        matches = re.findall(expr, line)
        for match in matches:
            if int(match[0]) > max_counts[match[1]]:
                possible = False
                break
                
        if possible:
            total += int(line.split(":")[0].split("Game ")[1])
    
    print("Part one answer:", total)


def part_two(data: str):
    total = 0
    expr = r'(\d+) (blue|red|green)'

    for line in data.splitlines():
        max_counts = {'red': 0, 'green': 0, 'blue': 0 }
        matches = re.findall(expr, line)
        for match in matches:
            if int(match[0]) > max_counts[match[1]]:
                max_counts[match[1]] = int(match[0])
        
        total += max_counts['red'] * max_counts['green'] * max_counts['blue']
                
    print("Part two answer:", total)


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        puzzle_input = f.read()
    part_one(puzzle_input)
    part_two(puzzle_input)