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


def parse_input_part_2(input_file: str) -> Tuple[List[int], List[int]]:
    with open(input_file, "rt", encoding="utf-8") as infile:
        _, instructions, *_ = infile.readlines()

    bus_ids: List[int] = []
    offsets = []
    offset = 1
    for item in instructions.split(","):
        if item == "x":
            offset += 1
        else:
            if bus_ids:
                offsets.append(offset)
            bus_ids.append(int(item))
            offset = 1

    return bus_ids, offsets


def find_timestamp(
    base_timestamp: int, first_bus_id: int, second_bus_id: int, offset: int
) -> Tuple[int, int]:
    """Find timestamp in which second bus will be offset ahead from the first bus.

    Start at base timestamp.
    """
    timestamp = base_timestamp
    while True:
        if (timestamp + offset) % second_bus_id == 0:
            return timestamp + offset, first_bus_id * second_bus_id
        timestamp += first_bus_id


def earliest_timestamp(bus_ids: List[int], offsets: List[int]) -> int:
    first_bus_id = bus_ids[0]
    base_timestamp = 0
    for second_bus_id, offset in zip(bus_ids[1:], offsets):
        base_timestamp, first_bus_id = find_timestamp(
            base_timestamp, first_bus_id, second_bus_id, offset
        )

    return base_timestamp - sum(offsets)


def main() -> None:
    parse_input_part_2(INPUT)
    instructions_1 = parse_input_part_1(INPUT)
    print(
        f"Product of ID and waiting time: {math.prod(earliest_bus(*instructions_1))}"
    )  # 2845

    instructions_2 = parse_input_part_2(INPUT)
    print(
        f"Earliest timestamp: {earliest_timestamp(*instructions_2)}"
    )  # 487905974205117


if __name__ == "__main__":
    main()
