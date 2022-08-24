#!/usr/bin/env python3
"""--- Day 12: Rain Risk ---
https://adventofcode.com/2020/day/12"""
from typing import List, Tuple

INPUT = "aoc2020_12_input.txt"
T_COORDINATES = Tuple[int, int]
T_INSTRUCTION = Tuple[str, int]


def rotate_ship(direction: str, value: int, orientation: str) -> str:
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


def rotate_waypoint(
    direction: str, value: int, position: T_COORDINATES
) -> T_COORDINATES:
    x, y = position
    for _ in range(value // 90):
        if direction == "L":
            x, y = y, -x
        elif direction == "R":
            x, y = -y, x
        else:
            raise ValueError(f"Invalid direction {direction!r}")

    return x, y


def move_to_waypoint(
    value: int, ship_position: T_COORDINATES, waypoint_position: T_COORDINATES
) -> T_COORDINATES:
    wx, wy = waypoint_position
    sx, sy = ship_position
    return wx * value + sx, wy * value + sy


def move(
    direction: str, value: int, position: T_COORDINATES, orientation: str
) -> T_COORDINATES:
    directions = {"E": (1, 0), "N": (0, -1), "W": (-1, 0), "S": (0, 1)}
    if direction in directions:
        dx, dy = directions[direction]
    elif direction == "F":
        dx, dy = directions[orientation]
    else:
        raise ValueError((f"Incorrect direction {direction!r}"))
    x, y = position

    return x + dx * value, y + dy * value


def move_ship_part_1(
    position: T_COORDINATES, orientation: str, instructions: List[T_INSTRUCTION]
) -> Tuple[T_COORDINATES, str]:
    if orientation not in "ENWS":
        raise ValueError(f"Incorrect orientation {orientation!r}")

    for action, value in instructions:
        if action in "LR":
            orientation = rotate_ship(action, value, orientation)
        elif action in "ENWSF":
            position = move(action, value, position, orientation)
        else:
            raise ValueError(f"Incorrect action: {action!r}")

    return position, orientation


def move_ship_part_2(
    position: T_COORDINATES, instructions: List[T_INSTRUCTION]
) -> Tuple[T_COORDINATES, T_COORDINATES]:
    ship_position = (0, 0)
    waypoint_position = position
    for action, value in instructions:
        if action in "ENWS":
            waypoint_position = move(action, value, waypoint_position, "")
        elif action == "F":
            ship_position = move_to_waypoint(value, ship_position, waypoint_position)
        elif action in "LR":
            waypoint_position = rotate_waypoint(action, value, waypoint_position)
        else:
            raise ValueError(f"Incorrect action: {action!r}")

    return ship_position, waypoint_position


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        instructions = [(line[0], int(line[1:])) for line in infile]

    ship_coordinates = move_ship_part_1((0, 0), "E", instructions)[0]
    distance = sum(abs(n) for n in ship_coordinates)
    print(f"Distance part 1: {distance}")  # 2280

    ship_coordinates = move_ship_part_2((10, -1), instructions)[0]
    distance = sum(abs(n) for n in ship_coordinates)
    print(f"Distance part 2: {distance}")  # 38693


if __name__ == "__main__":
    main()
