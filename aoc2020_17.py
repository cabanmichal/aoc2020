#!/usr/bin/env python3
"""--- Day 17: Conway Cubes ---
https://adventofcode.com/2020/day/17"""

INPUT = "aoc2020_17_input.txt"
ACTIVE = "#"
INACTIVE = "."
T_CUBE = tuple[int, int, int]


def load_input(input_file: str) -> tuple[set[T_CUBE], tuple[int, int]]:
    active_cubes = set()
    z = 0
    size = 0
    with open(input_file, "rt", encoding="utf-8") as infile:
        for y, line in enumerate(infile):
            line = line.strip()
            size = len(line)
            for x, cube in enumerate(line):
                if cube == ACTIVE:
                    active_cubes.add((x, y, z))
    return active_cubes, (0, size)


def adjacent_cubes(cube: T_CUBE) -> set[T_CUBE]:
    cubes = set()
    differences = (-1, 0, 1)
    x, y, z = cube
    for dx in differences:
        for dy in differences:
            for dz in differences:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                cubes.add((x + dx, y + dy, z + dz))
    return cubes


def cycle(active_cubes: set[T_CUBE], range_: tuple[int, int]) -> set[T_CUBE]:
    new_active_cubes = set()
    for x in range(*range_):
        for y in range(*range_):
            for z in range(*range_):
                cube = (x, y, z)
                active_neighbours = active_cubes & adjacent_cubes(cube)
                if cube in active_cubes:
                    if 2 <= len(active_neighbours) <= 3:
                        new_active_cubes.add(cube)
                elif len(active_neighbours) == 3:
                    new_active_cubes.add(cube)
    return new_active_cubes


def cycle_n_times(
    active_cubes: set[T_CUBE], range_: tuple[int, int], n: int
) -> set[T_CUBE]:
    start, end = range_
    for _ in range(n):
        active_cubes = cycle(active_cubes, (start, end))
        start -= 1
        end += 1
    return active_cubes


def main() -> None:
    print(cycle_n_times(*load_input(INPUT), 6))
    print(adjacent_cubes((1, 2, 3)))


if __name__ == "__main__":
    main()
