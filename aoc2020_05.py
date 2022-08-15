#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/5"""
from typing import List

INPUT = "aoc2020_05_input.txt"


def _find_position(navigation: str, left: str, right: str) -> int:
    start = 0
    end = 2 ** len(navigation) - 1

    for direction in navigation:
        if direction == left:
            end = (start + end + 1) // 2 - 1
        elif direction == right:
            start = (start + end + 1) // 2
        else:
            raise ValueError(f"Incorrect direction: {direction!r}")

    return start


def find_row(navigation: str) -> int:
    return _find_position(navigation, left="F", right="B")


def find_column(navigation: str) -> int:
    return _find_position(navigation, left="L", right="R")


def get_seat_id(row: int, column: int) -> int:
    return row * 8 + column


def seat_id_from_navigation(navigation: str) -> int:
    return get_seat_id(find_row(navigation[:7]), find_column(navigation[7:]))


def find_seat_id(seat_ids: List[int]) -> int:
    sorted_ids = sorted(seat_ids)
    for idx, seat_id in enumerate(sorted_ids[:-1]):
        if sorted_ids[idx + 1] - seat_id == 2:
            return seat_id + 1
    return -1


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        seat_ids = [seat_id_from_navigation(line.strip()) for line in infile]

    print(f"Highest seat ID: {max(seat_ids)}")  # 922
    print(f"My seat ID: {find_seat_id(seat_ids)}")  # 747


if __name__ == "__main__":
    main()
