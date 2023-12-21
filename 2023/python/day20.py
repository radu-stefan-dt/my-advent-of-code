import sys
from typing import List, Dict, Union

MODULES = {}


def parse_input(puzzle_input: str) -> List[str]:
    broadcast = None

    # Parse input and create modules
    for line in puzzle_input.splitlines():
        source, destinations = line.split(" -> ")
        if source[0] == "%":
            MODULES[source[1:]] = [source[0], "off", destinations.split(", ")]
        elif source[0] == "&":
            MODULES[source[1:]] = [source[0], {}, destinations.split(", ")]
        elif source == "broadcaster":
            broadcast = destinations.split(", ")

    # Parse again and load state for '&' modules
    for line in puzzle_input.splitlines():
        source, destinations = line.split(" -> ")
        if source != "broadcaster":
            for dest_module in destinations.split(", "):
                if dest_module in MODULES and MODULES[dest_module][0] == "&":
                    MODULES[dest_module][1][source[1:]] = "low"

    return broadcast


def send_pulse(src: str, dest: str, pulse: str):
    # Handle untyped module for testing
    if dest not in MODULES:
        return []

    # Flip flop module
    if MODULES[dest][0] == "%":
        # Only low pulses do anything
        if pulse == "low":
            # Flip the state
            MODULES[dest][1] = "on" if MODULES[dest][1] == "off" else "off"
            # Send high pulse if on, otherwise low
            next_pulse = "high" if MODULES[dest][1] == "on" else "low"
            return [(dest, next_dest, next_pulse) for next_dest in MODULES[dest][2]]
        return []
    
    # Conjunction module - update the last pulse for source
    if src != "broadcaster":
        MODULES[dest][1][src] = pulse
    # Then, send low pulse if all states are high, otherwise send high pulse
    next_pulse = "low" if set(MODULES[dest][1].values()) == {"high"} else "high"
    return [(dest, next_dest, next_pulse) for next_dest in MODULES[dest][2]]


def part_one(broadcast: List[str]) -> int:
    high_pulses = 0
    low_pulses = 0
    for _ in range(1000):
        low_pulses += 1 + len(broadcast)
        queue = [("broadcaster", dest, "low") for dest in broadcast]
        while len(queue) > 0:
            new_pulses = send_pulse(*queue.pop(0))
            high_pulses += len([p for p in new_pulses if p[2] == "high"])
            low_pulses += len([p for p in new_pulses if p[2] == "low"])
            queue.extend(new_pulses)

    return high_pulses*low_pulses


def solve_puzzle(puzzle_input: str):
    broadcast = parse_input(puzzle_input)
    result = part_one(broadcast)
    print("Part one result:", result)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
