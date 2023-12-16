import sys
from functools import reduce
from typing import List, Dict


def get_score(line: str):
    total = 0
    card_def, played_str = line.split("|")
    winning_str = card_def.split(":")[1]
    winning_nums = winning_str.split()
    played_nums = played_str.split()

    won_plays = len([num for num in played_nums if num in winning_nums])

    if won_plays > 1:
        total += 2 ** (won_plays - 1)
    elif won_plays == 1:
        total += 1

    return total


def process_original_cards(data: str) -> Dict[int, dict]:
    cards = {}

    for line in data.splitlines():
        card_def, played_str = line.split("|")
        card_id, winning_str = card_def.split(":")
        winning_nums = winning_str.split()
        played_nums = played_str.split()
        won_copies = len([num for num in played_nums if num in winning_nums])
        num_id = int(card_id.replace("Card ", ""))
        cards[num_id] = {"id": num_id, "won_copies": won_copies}

    return cards


def get_won_cards(originals: dict, card: dict):
    total = 0

    copy_ids = [card["id"] + i for i in range(1, card["won_copies"] + 1)]
    total += len(copy_ids)
    if len(copy_ids) == 0:
        return total
    else:
        for won_id in copy_ids:
            total += get_won_cards(originals, originals[won_id])

    return total


def solve_puzzle(data: str):
    result1 = sum([get_score(line) for line in data.splitlines()])
    print("Part one answer:", result1)

    original_cards = process_original_cards(data)

    result2 = reduce(
        lambda a, b: a + b,
        [get_won_cards(original_cards, card) for _, card in original_cards.items()],
        len(original_cards.keys()),
    )

    print("Part two answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()

    solve_puzzle(puzzle_input)
