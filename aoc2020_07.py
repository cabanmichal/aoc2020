#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/7"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

INPUT = "aoc2020_07_input.txt"

RULES = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip().splitlines(
    keepends=False
)


_rule_pattern = re.compile(
    r"""
        ^ (?P<bag>.+?)\ bag                         # first bag
        | (?P<capacity>\d+)\ (?P<sub_bag>.+?)\ bag  # bags it contains
    """,
    re.VERBOSE,
)


@dataclass
class Bag:
    name: str
    parents: List["Bag"] = field(default_factory=list)
    children: List[Tuple["Bag", int]] = field(default_factory=list)

    def add_parent(self, bag: "Bag") -> None:
        self.parents.append(bag)

    def add_child(self, bag: "Bag", capacity: int) -> None:
        self.children.append((bag, capacity))


def build_relationship_graph(rules: List[str]) -> Dict[str, Bag]:
    graph: Dict[str, Bag] = {}
    for rule in rules:
        matches = _rule_pattern.finditer(rule)
        bag_name = next(matches).group("bag")
        bag = graph.setdefault(bag_name, Bag(bag_name))

        for match in matches:
            capacity = int(match.group("capacity"))
            sub_bug_name = match.group("sub_bag")
            sub_bag = graph.setdefault(sub_bug_name, Bag(sub_bug_name))
            bag.add_child(sub_bag, capacity)
            sub_bag.add_parent(bag)

    return graph


def count_bags_that_can_contain_bag(graph: Dict[str, Bag], bag_name: str) -> int:
    bags = set()

    def traverse(bag: Bag) -> None:
        for parent in bag.parents:
            bags.add(parent.name)
            traverse(parent)

    traverse(graph[bag_name])

    return len(bags)


def count_bags_needed(graph: Dict[str, Bag], bag_name: str) -> int:
    def traverse(bag: Bag, count: int = 1) -> int:
        for child, num in bag.children:
            count += traverse(child, count + num)

        return count

    return traverse(graph[bag_name])


def main() -> None:
    graph = build_relationship_graph(RULES)
    # with open(INPUT, "rt", encoding="utf-8") as infile:
    #     graph = build_relationship_graph(infile.readlines())
    count = count_bags_that_can_contain_bag(graph, "shiny gold")
    print(count)
    count = count_bags_needed(graph, "shiny gold")
    print(count)


if __name__ == "__main__":
    main()
