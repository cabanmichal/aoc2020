#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/13"""


import math
from typing import List, Tuple

INPUT = "aoc2020_13_input.txt"


def parse_input_part_1(input_file: str) -> Tuple[int, List[int]]:
    with open(input_file, "rt", encoding="utf-8") as infile:
        timestamp, buses, *_ = infile.readlines()
        bus_ids = [int(bus) for bus in buses.split(",") if bus != "x"]

        return int(timestamp), bus_ids


def earliest_bus(timestamp: int, buses: List[int]) -> Tuple[int, int]:
    wait_times = []
    for bus in buses:
        if timestamp / bus == 0:
            wait_times.append(0)
        else:
            wait_times.append((timestamp // bus + 1) * bus - timestamp)

    min_wait_time = min(wait_times)
    min_wait_time_bus = buses[wait_times.index(min_wait_time)]

    return min_wait_time_bus, min_wait_time


def main() -> None:
    instructions = parse_input_part_1(INPUT)
    print(
        f"Product of ID and waiting time: {math.prod(earliest_bus(*instructions))}"
    )  # 2845


if __name__ == "__main__":
    main()
