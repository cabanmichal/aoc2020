#!/usr/bin/env python3
"""--- Day 17: Conway Cubes ---
https://adventofcode.com/2020/day/17"""

import itertools

INPUT = "aoc2020_17_input.txt"
ACTIVE = "#"
T_SQUARE = tuple[int, int]
T_CUBE = tuple[int, ...]


def load_input(input_file: str) -> tuple[set[T_SQUARE], tuple[int, int]]:
    active_cubes = set()
    size = 0
    with open(input_file, "rt", encoding="utf-8") as infile:
        for y, line in enumerate(infile):
            line = line.strip()
            size = len(line)
            for x, cube in enumerate(line):
                if cube == ACTIVE:
                    active_cubes.add((x, y))

    return active_cubes, (-1, size + 1)


def format_squares_as_cubes(squares: set[T_SQUARE], dimension: int) -> set[T_CUBE]:
    return {(x, y, *(0,) * (dimension - 2)) for x, y in squares}


def adjacent_cubes(cube: T_CUBE, dimension: int) -> set[T_CUBE]:
    cubes: set[tuple[int, ...]] = set()
    differences = (-1, 0, 1)
    for coordinate_differences in itertools.product(differences, repeat=dimension):
        if not any(coordinate_differences):  # all 0s => the cube itself
            continue
        adjacent_cube = tuple(
            coordinate + difference
            for coordinate, difference in zip(cube, coordinate_differences)
        )
        cubes.add(adjacent_cube)

    return cubes


def cycle_cubes(
    active_cubes: set[T_CUBE], range_: tuple[int, int], dimension: int
) -> set[T_CUBE]:
    new_active_cubes: set[tuple[int, ...]] = set()
    start, end = range_

    for cube in itertools.product(range(start, end), repeat=dimension):
        active_neighbours = active_cubes & adjacent_cubes(cube, dimension)
        if cube in active_cubes:
            if 2 <= len(active_neighbours) <= 3:
                new_active_cubes.add(cube)
        elif len(active_neighbours) == 3:
            new_active_cubes.add(cube)

    return new_active_cubes


def cycle_cubes_n_times(
    active_cubes: set[T_CUBE], range_: tuple[int, int], n: int, dimension: int
) -> set[T_CUBE]:
    start, end = range_
    for _ in range(n):
        active_cubes = cycle_cubes(active_cubes, (start, end), dimension)
        start -= 1
        end += 1

    return active_cubes


def main() -> None:
    squares, range_ = load_input(INPUT)
    active_cubes = len(
        cycle_cubes_n_times(format_squares_as_cubes(squares, 3), range_, 6, 3)
    )
    print(f"Active cubes after 6th cycle: {active_cubes}")  # 319

    active_cubes = len(
        cycle_cubes_n_times(format_squares_as_cubes(squares, 4), range_, 6, 4)
    )
    print(f"Active cubes after 6th cycle: {active_cubes}")  # 2324


if __name__ == "__main__":
    main()
