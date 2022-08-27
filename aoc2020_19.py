#!/usr/bin/env python3
"""--- Day 19: Monster Messages ---
https://adventofcode.com/2020/day/19"""

import itertools
from dataclasses import dataclass, field

INPUT = "aoc2020_19_input.txt"


@dataclass
class Rule:
    name: str
    subrules: list[list["Rule"]] = field(default_factory=list)

    def expand(self) -> list[str]:
        expanded = []
        if not self.subrules:
            return [self.name]
        for group in self.subrules:
            for item in itertools.product(*(rule.expand() for rule in group)):
                expanded.append("".join(item))
        return expanded


def parse_rules(unparsed_rules: list[str]) -> dict[str, Rule]:
    parsed: dict[str, Rule] = {}
    for unparsed_rule in unparsed_rules:
        parts = unparsed_rule.replace('"', "").replace(":", "").split()
        groups = []
        group: list[Rule] = []
        for item in parts[1:]:
            if item == "|" and group:
                groups.append(group)
                group = []
            else:
                rule = parsed.setdefault(item, Rule(item))
                group.append(rule)
        if group:
            groups.append(group)

        rule = parsed.setdefault(parts[0], Rule(parts[0]))
        rule.subrules.extend(groups)

    return parsed


def expand_rules(parsed_rules: dict[str, Rule]) -> dict[int, list[str]]:
    expanded = {}
    for rule in parsed_rules.values():
        if rule.subrules:
            expanded[int(rule.name)] = rule.expand()

    return expanded


def load_input(input_file: str) -> tuple[dict[int, list[str]], list[str]]:
    with open(input_file, "rt", encoding="utf-8") as infile:
        rules_part, messages_part = infile.read().strip().split("\n\n")

    rules = expand_rules(parse_rules(rules_part.splitlines(keepends=False)))

    return rules, messages_part.splitlines(keepends=False)


def count_matching_messages(messages: list[str], rules: list[str]) -> int:
    count = 0
    for message in messages:
        if message in rules:
            count += 1
    return count


def main() -> None:
    rules, messages = load_input(INPUT)
    print(count_matching_messages(messages, rules[0]))


if __name__ == "__main__":
    main()
