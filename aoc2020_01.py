#!/usr/bin/env python3
"""--- Day 1: Report Repair ---
https://adventofcode.com/2020/day/1"""
import bisect
import math
from typing import List

INPUT = "aoc2020_01_input.txt"
SUM = 2020


def load_entries(report_file: str) -> List[int]:
    with open(report_file, "rt", encoding="utf-8") as infile:
        return list(map(int, infile.readlines()))


def number_in_list(numbers: List[int], number: int, start: int = 0) -> bool:
    idx = bisect.bisect_left(numbers, number, lo=start)
    return idx != len(numbers) and numbers[idx] == number


def find_n_entries(numbers: List[int], n: int, total: int) -> List[int]:
    if n < 1:
        raise ValueError("n should be 1 or higher")

    selected: List[int] = []

    def find(start: int = 0) -> bool:
        if len(selected) == n - 1:
            remaining = total - sum(selected)
            if number_in_list(numbers, remaining, start):
                selected.append(remaining)
                return True
            return False

        for idx, number in enumerate(numbers[start:]):
            selected.append(number)
            completed = find(start=start + idx + 1)
            if completed:
                return True
            selected.pop()

        return False

    find()

    return selected


def main() -> None:
    numbers = sorted(load_entries(report_file=INPUT))

    entries = find_n_entries(numbers, 2, SUM)
    print("Found entries:", entries, math.prod(entries))  # 100419

    entries = find_n_entries(numbers, 3, SUM)
    print("Found entries:", entries, math.prod(entries))  # 265253940


if __name__ == "__main__":
    main()
