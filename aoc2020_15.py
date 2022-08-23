#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/15"""


INPUT = "aoc2020_15_input.txt"


def play(numbers: list[int], rounds: int) -> int:
    turns = 0
    state: dict[int, tuple[int, int]] = {}
    spoken_before = False

    while turns < rounds:
        turns += 1

        if turns <= len(numbers):
            last_spoken = numbers[turns - 1]
        elif spoken_before:
            before_last, last = state[last_spoken]
            last_spoken = last - before_last
        else:
            last_spoken = 0

        spoken_before = last_spoken in state
        if spoken_before:
            _, last = state[last_spoken]
            state[last_spoken] = (last, turns)
        else:
            state[last_spoken] = (0, turns)

    return last_spoken


def load_starting_numbers(filename: str) -> list[int]:
    with open(filename, "rt", encoding="utf-8") as infile:
        first_line, *_ = infile.readlines()

        return [int(number) for number in first_line.split(",")]


def main() -> None:
    numbers = load_starting_numbers(INPUT)
    print(f"2020th number spoken: {play(numbers, 2020)}")  # 412
    print(f"30000000th number spoken: {play(numbers, 30000000)}")  # 243


if __name__ == "__main__":
    main()
