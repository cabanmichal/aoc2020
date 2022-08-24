#!/usr/bin/env python3
"""--- Day 6: Custom Customs ---
https://adventofcode.com/2020/day/6"""

INPUT = "aoc2020_06_input.txt"


def count_yes_answered_in_group_by_anyone(group_answers: list[str]) -> int:
    return len(set("".join(group_answers)))


def count_yes_answered_in_group_by_everyone(group_answers: list[str]) -> int:
    return len(set.intersection(*(set(answers) for answers in group_answers)))


def load_groups_from_input(input_file: str) -> list[list[str]]:
    groups: list[list[str]] = []
    group: list[str] = []

    with open(input_file, "rt", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if not line and group:
                groups.append(group)
                group = []
                continue
            group.append(line)

        if group:
            groups.append(group)

    return groups


def main() -> None:
    sum_of_counts_1 = 0
    sum_of_counts_2 = 0
    for group in load_groups_from_input(INPUT):
        sum_of_counts_1 += count_yes_answered_in_group_by_anyone(group)
        sum_of_counts_2 += count_yes_answered_in_group_by_everyone(group)

    print(f"Sum of counts of 'yes' answers (anyone): {sum_of_counts_1}")  # 6768
    print(f"Sum of counts of 'yes' answers (everyone): {sum_of_counts_2}")  # 3489


if __name__ == "__main__":
    main()
