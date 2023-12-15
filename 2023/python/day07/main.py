import sys
from typing import List


def part_one(lines: List[str]):
    games = []
    for line in lines:
        hand, str_bid = line.split()
        # Highest number of cards of 1 kind
        card_copies = max(map(hand.count, hand))
        # The number of card kinds
        unique_cards = len(set(hand))
        # Games values for each card
        cards_to_values = map("23456789TJQKA".index, hand)
        games.append((card_copies, -unique_cards, *cards_to_values, int(str_bid)))
    
    result = sum((i + 1) * bid for i, (*_, bid) in enumerate(sorted(games)))
    print("Part one answer:", result)


def part_two(lines: List[str]):
    games = []
    for line in lines:
        hand, str_bid = line.split()
        # J can be any card
        card_copies = max(map(
            lambda x: (hand.count(x) if x != "J" else 0) + hand.count("J"),
            hand
        ))
        # Don't count J as unique card
        unique_cards = len(set(hand.replace("J", ""))) or 1
        # J is lowest value
        cards_to_values = map("J23456789TQKA".index, hand)
        games.append((card_copies, -unique_cards, *cards_to_values, int(str_bid)))

    result = sum((i + 1) * bid for i, (*_, bid) in enumerate(sorted(games)))
    print("Part two answer:", result)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read().splitlines()
    part_one(puzzle_input)
    part_two(puzzle_input)