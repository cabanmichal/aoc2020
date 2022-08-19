#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/12"""
from typing import List, Tuple

INPUT = "aoc2020_12_input.txt"


def turn(direction: str, value: int, orientation: str) -> str:
    directions = "ENWS"
    if orientation not in directions:
        raise ValueError(f"Incorrect orientation {orientation!r}")

    steps = value // 90
    if direction == "L":
        sign = 1
    elif direction == "R":
        sign = -1
    else:
        raise ValueError(f"Invalid direction {direction!r}")
    index = (directions.index(orientation) + sign * steps) % len(directions)

    return directions[index]


def move(
    direction: str, value: int, position: Tuple[int, int], orientation: str
) -> Tuple[int, int]:
    directions = {"E": (1, 0), "N": (0, -1), "W": (-1, 0), "S": (0, 1)}
    if direction in directions:
        dx, dy = directions[direction]
    elif direction == "F":
        dx, dy = directions[orientation]
    else:
        raise ValueError((f"Incorrect direction {direction!r}"))
    x, y = position

    return x + dx * value, y + dy * value


def move_ship(
    position: Tuple[int, int], orientation: str, instructions: List[Tuple[str, int]]
) -> Tuple[Tuple[int, int], str]:
    if orientation not in "ENWS":
        raise ValueError(f"Incorrect orientation {orientation!r}")

    for direction, value in instructions:
        if direction in "LR":
            orientation = turn(direction, value, orientation)
        elif direction in "ENWSF":
            position = move(direction, value, position, orientation)
        else:
            raise ValueError(f"Incorrect direction: {direction!r}")

    return position, orientation


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        instructions = [(line[0], int(line[1:])) for line in infile]

    distance_1 = sum(move_ship((0, 0), "E", instructions)[0])
    print(f"Distance part 1: {distance_1}")


if __name__ == "__main__":
    main()
