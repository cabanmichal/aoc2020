#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/2"""
import re
from dataclasses import dataclass
from typing import Type, TypeVar

INPUT = "aoc2020_02_input.txt"
T = TypeVar("T", bound="Record")

_pattern = re.compile(r"(\d+)-(\d+) (.): (.+)")


@dataclass
class Record:
    min_count: int
    max_count: int
    character: str
    password: str

    @classmethod
    def from_password_list_line(cls: Type[T], line: str) -> T:
        match = _pattern.search(line)
        if match is None:
            raise ValueError(f"Cannot parse line: {line!r}")

        min_count, max_count, character, password, *_ = match.groups()
        return cls(int(min_count), int(max_count), character, password)

    def is_valid_policy_1(self) -> bool:
        count = self.password.count(self.character)
        return self.min_count <= count <= self.max_count

    def is_valid_policy_2(self) -> bool:
        count = 0
        for number in (self.min_count, self.max_count):
            idx = number - 1
            if 0 <= idx < len(self.password) and self.password[idx] == self.character:
                count += 1

        return count == 1


def check_password_file(filename: str) -> None:
    valid_count_1 = 0
    valid_count_2 = 0
    with open(filename, "rt", encoding="utf-8") as infile:
        for line in infile:
            record = Record.from_password_list_line(line)
            if record.is_valid_policy_1():
                valid_count_1 += 1
            if record.is_valid_policy_2():
                valid_count_2 += 1

    print(f"Valid passwords: {valid_count_1} / {valid_count_2}")  # 469 / 267


def main() -> None:
    check_password_file(INPUT)


if __name__ == "__main__":
    main()
