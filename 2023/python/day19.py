import re
import sys
from typing import Tuple, List, Dict, Union


def parse_input(
    puzzle_input: str,
) -> Tuple[Dict[str, Dict[str, Union[List, str]]], List[Dict[str, int]]]:
    workflow_str, part_str = puzzle_input.split("\n\n")

    parts = []
    for part in part_str.splitlines():
        p = {}
        for item in part.replace("{", "").replace("}", "").split(","):
            attr, val = item.split("=")
            p[attr] = int(val)
        parts.append(p)

    workflows = {}
    for workflow in workflow_str.splitlines():
        name, details = workflow.replace("}", "").split("{")

        *rules, otherwise = details.split(",")
        workflows[name] = {"rules": [], "otherwise": otherwise}
        for rule in rules:
            condition, result = rule.split(":")
            workflows[name]["rules"].append((condition[0], condition[1:], result))

    return workflows, parts


def is_accepted(
    workflows: Dict[str, Dict[str, Union[List, str]]], part: Dict[str, int]
) -> bool:
    next_workflow = "in"
    while next_workflow not in "RA":
        for attr, eval_str, result in workflows[next_workflow]["rules"]:
            if eval(f"{part[attr]}{eval_str}"):
                next_workflow = result
                break
        else:
            next_workflow = workflows[next_workflow]["otherwise"]
    return next_workflow == "A"


def opposite(condition: str) -> str:
    attr, op, val = re.match(r'^(.)(.*?)(\d+)$', condition).groups()
    if op == ">":
        new_op = "<="
    elif op == "<":
        new_op = ">="
    elif op == ">=":
        new_op = "<"
    elif op == "<=":
        new_op = ">"
    
    return f"{attr}{new_op}{val}"
    

def parse_workflow(workflows: dict, name: str, trace: list = [], d=-1) -> str:
    conditions = []
    # Loop logic
    for attr, eval_str, result in workflows[name]["rules"]:
        if result == "R":
            trace.append(opposite(f"{attr}{eval_str}"))
        elif result == "A":
            combo = [*trace, f"{attr}{eval_str}"]
            conditions.append(combo)
            trace.append(opposite(f"{attr}{eval_str}"))
        else:
            fwd_trace = [*trace, f"{attr}{eval_str}"]
            conditions.extend(parse_workflow(workflows, result, fwd_trace, d))
            trace.append(opposite(f"{attr}{eval_str}"))
    
    # Exit conditions
    o = workflows[name]["otherwise"]
    if o == "R":
        return conditions
    elif o == "A":
        conditions.append(trace)
    else:
        conditions.extend(parse_workflow(workflows, o, trace, d))
    
    return conditions


def parse_condition(condition: List[str]):
    total_matches = 1
    for attr in 'xmas':
        range_min = 1
        range_max = 4000
        conditions = [c[1:] for c in condition if c.startswith(attr)]
        for c in conditions:
            op, val = re.match(r'^(.*?)(\d+)$', c).groups()
            if op in [">", ">="]:
                range_min = max(range_min, int(val)+(1 if op == ">" else 0))
            elif op in ["<", "<="]:
                range_max = min(range_max, int(val)-(1 if op == "<" else 0))
        total_matches *= range_max - range_min + 1
    return total_matches


def solve_puzzle(puzzle_input: str):
    workflows, parts = parse_input(puzzle_input)
    result = sum([sum(part.values()) for part in parts if is_accepted(workflows, part)])
    print("Part one result:", result)

    conditions = parse_workflow(workflows, "in")
    result2 = sum([parse_condition(c) for c in conditions])
    print("Part two result:", result2)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        puzzle_input = f.read()
    solve_puzzle(puzzle_input)
