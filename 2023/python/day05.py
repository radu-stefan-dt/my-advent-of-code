import sys
from typing import Tuple, Dict, List


def parse_input(
    data: str,
) -> Tuple[Tuple[int, int], Dict[str, List[Tuple[Tuple[int, int], int, str]]]]:
    seeds = []
    mapping = {}

    current_map, next_map = None, None
    for line in data.splitlines():
        # Skip empty lines
        if line == "":
            continue

        # Only one line with seed numbers
        if "seeds" in line:
            seeds = [int(n) for n in line.split("seeds:")[1].split()]

        # Map declares what the next lines define
        elif "map" in line:
            src_name, dest_name = line.split(" map:")[0].split("-to-")
            current_map = src_name
            next_map = dest_name
            mapping[current_map] = []

        # Regular lines add ranges to the current map
        else:
            dst_start, src_start, length = line.split()
            mapping[current_map].append(
                [
                    # The range of seeds accepted
                    [int(src_start), int(src_start) + int(length) - 1],
                    # The offset for converting to next map
                    int(dst_start) - int(src_start),
                    # The name of the next map
                    next_map,
                ]
            )

    return seeds, mapping


def get_location_for_seed(
    src: int, mapping: Dict[str, List[Tuple[Tuple[int, int], int, str]]]
):
    next_map = "seed"
    while next_map != "location":
        map_details = mapping[next_map]
        for detail in map_details:
            # If our src is in the ranges of the map, break out
            if src >= detail[0][0] and src <= detail[0][1]:
                # Convert the seed using the offset
                src = src + detail[1]
                next_map = detail[2]
                break
        # If src not listed, keep same number and move to next map
        else:
            next_map = detail[2]

        # If we're at the location map, check if we're the new min
        if next_map == "location":
            return src


def merge_overlapping_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    ranges.sort(key=lambda r: r[0])

    merged_ranges = [ranges[0]]
    for r in ranges[1:]:
        if merged_ranges[-1][0] <= r[0] <= merged_ranges[-1][-1]:
            merged_ranges[-1][-1] = max(merged_ranges[-1][-1], r[-1])
        else:
            merged_ranges.append(r)

    return merged_ranges


def convert_seeds_for_next_map(
    current_map: List[Tuple[Tuple[int, int], int, str]], seeds: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    new_seeds = []
    while len(seeds) > 0:
        seed_range = seeds.pop(0)

        converted = False
        for map_range in current_map:
            seed_start = seed_range[0]
            seed_end = seed_range[1]
            map_start = map_range[0][0]
            map_end = map_range[0][1]
            offset = map_range[1]

            # If seed range is contained fully
            if seed_start >= map_start and seed_end <= map_end:
                converted = True
                new_seeds.append([seed_start + offset, seed_end + offset])

            # If seed range start is outside of map range, but end is contained
            elif (
                seed_start < map_start and seed_end >= map_start and seed_end <= map_end
            ):
                converted = True
                new_seeds.append([map_start + offset, seed_end + offset])
                seeds.append([seed_start, map_start - 1])

            # If seed range end is outside of map range, but start is contained
            elif (
                seed_end > map_end and seed_start >= map_start and seed_start <= map_end
            ):
                converted = True
                new_seeds.append([seed_start + offset, map_end + offset])
                seeds.append([map_end + 1, seed_end])

            # If seed range contains map range
            elif seed_start < map_start and seed_end > map_end:
                converted = True
                new_seeds.append([map_start + offset, map_end + offset])
                seeds.append([seed_start, map_start - 1])
                seeds.append([map_end + 1, seed_end])

        # Anything that can't convert, keeps the same value
        if not converted:
            new_seeds.append(seed_range)

    # Before returning, merge any overlapping ranges
    return merge_overlapping_ranges(new_seeds)


def solve_puzzle(
    seeds: List[int], mapping: Dict[str, List[Tuple[Tuple[int, int], int, str]]]
) -> int:
    result1 = min([get_location_for_seed(src, mapping) for src in seeds])
    print("Part one answer:", result1)

    # Process seeds into ranges
    seed_starts = seeds[::2]
    range_lengths = seeds[1::2]
    seed_ranges = [
        [seed_starts[i], seed_starts[i] + range_lengths[i] - 1]
        for i in range(len(seed_starts))
    ]

    # Convert seeds to location map
    next_map = "seed"
    while next_map != "location":
        map_details = mapping[next_map]
        seed_ranges = convert_seeds_for_next_map(map_details, seed_ranges)
        next_map = map_details[0][2]

    result2 = min([seed_range[0] for seed_range in seed_ranges])
    print("Part two answer:", result2)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        puzzle_input = f.read()
    seeds, mapping = parse_input(puzzle_input)
    solve_puzzle(seeds, mapping)
