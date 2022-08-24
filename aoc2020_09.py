#!/usr/bin/env python3
"""--- Day 9: Encoding Error ---
https://adventofcode.com/2020/day/9"""

from aoc2020_01 import find_n_entries

INPUT = "aoc2020_09_input.txt"
PREAMBLE = 25


def find_error(data: list[int], preamble: int) -> int:
    for head, number in enumerate(data[preamble:], start=preamble):
        if not find_n_entries(sorted(data[head - preamble : head]), 2, number):
            return number
    return 0


def find_contiguous_set(numbers: list[int], value: int) -> list[int]:
    start, end = 0, 1
    total = numbers[start]

    while start < end and end < len(numbers):
        if total < value:
            total += numbers[end]
            end += 1
        elif total > value:
            total -= numbers[start]
            start += 1
        elif end - start == 1:  # correct sum but only one number
            start += 1
            end += 1
            total = numbers[start]
        else:
            return numbers[start:end]
    raise ValueError(f"No contigous set has sum of {value}")


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        numbers = [int(number) for number in infile]

    error = find_error(numbers, PREAMBLE)
    contiguous_set = find_contiguous_set(numbers, error)
    weakness = min(contiguous_set) + max(contiguous_set)

    print(f"First invalid number: {error}")  # 400480901
    print(f"Encryption weakness: {weakness}")  # 67587168


if __name__ == "__main__":
    main()
