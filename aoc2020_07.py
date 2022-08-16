#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/7"""
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

INPUT = "aoc2020_07_input.txt"
_rule_pattern = re.compile(
    r"""
        ^ (?P<bag>.+?)\ bag                       # first bag
        | (?P<amount>\d+)\ (?P<sub_bag>.+?)\ bag  # bags it contains
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

    def add_child(self, bag: "Bag", amount: int) -> None:
        self.children.append((bag, amount))


def build_graph(rules: List[str]) -> Dict[str, Bag]:
    graph: Dict[str, Bag] = {}
    for rule in rules:
        matches = _rule_pattern.finditer(rule)
        bag_name = next(matches).group("bag")
        bag = graph.setdefault(bag_name, Bag(bag_name))

        for match in matches:
            amount = int(match.group("amount"))
            sub_bag_name = match.group("sub_bag")
            sub_bag = graph.setdefault(sub_bag_name, Bag(sub_bag_name))
            bag.add_child(sub_bag, amount)
            sub_bag.add_parent(bag)

    return graph


def count_bags_that_can_contain_bag(graph: Dict[str, Bag], bag_name: str) -> int:
    def traverse(bag: Bag) -> Set[str]:
        bags = {bag.name}
        for parent in bag.parents:
            bags.update(traverse(parent))
        return bags

    return len(traverse(graph[bag_name])) - 1


def count_bags_needed(graph: Dict[str, Bag], bag_name: str) -> int:
    def traverse(bag: Bag) -> int:
        count = 1
        for child, num in bag.children:
            count += num * traverse(child)
        return count

    return traverse(graph[bag_name]) - 1


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        graph = build_graph(infile.readlines())

    bag_name = "shiny gold"
    count_can_contain = count_bags_that_can_contain_bag(graph, bag_name)
    count_needed = count_bags_needed(graph, bag_name)
    print(f"Numbers of bags: {count_can_contain} / {count_needed}")  # 208 / 1664


if __name__ == "__main__":
    main()
