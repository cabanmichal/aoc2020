#!/usr/bin/env python3
"""--- Day 10: Adapter Array ---
https://adventofcode.com/2020/day/10"""

import itertools
import math
from collections import defaultdict
from typing import Iterator

INPUT = "aoc2020_10_input.txt"


def count_differences(adapters: list[int]) -> dict[int, int]:
    differences: dict[int, int] = defaultdict(int)
    last_adapter = adapters[0]
    for adapter in adapters[1:]:
        difference = adapter - last_adapter
        differences[difference] += 1
        last_adapter = adapter
    differences[3] += 1  # device's built-in adapter

    return differences


def droppable_adapters(adapters: list[int]) -> Iterator[list[int]]:
    start = 0
    end = 2
    group = []
    while end < len(adapters):
        if adapters[end] - adapters[start] <= 3:
            group.append(start + 1)
        elif group:
            yield group
            group = []
        start += 1
        end += 1

    if group:
        yield group


def adapter_configurations(adapters: list[int]) -> Iterator[list[int]]:
    switches = [0, 1]
    for configuration in itertools.product(switches, repeat=len(adapters)):
        yield list(itertools.compress(adapters, configuration))


def can_drop(adapters: list[int], to_drop: list[int]) -> bool:
    if not to_drop:
        return True

    start = to_drop[0] - 1
    end = to_drop[-1] + 2
    plugged = [
        adapter
        for idx, adapter in enumerate(adapters[start:end], start=start)
        if idx not in to_drop
    ]

    last_adapter = plugged[0]
    for adapter in plugged[1:]:
        if adapter - last_adapter > 3:
            return False
        last_adapter = adapter

    return True


def count_distinct_adapter_chains(adapters: list[int]) -> int:
    ways_to_plug_withing_group = []
    for group in droppable_adapters(adapters):
        droppable_configurations = 0
        for configuration in adapter_configurations(group):
            if can_drop(adapters, configuration):
                droppable_configurations += 1
        ways_to_plug_withing_group.append(droppable_configurations)

    return math.prod(ways_to_plug_withing_group)


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        adapters = [int(line.strip()) for line in infile]

    adapters = [0] + sorted(adapters)
    differences = count_differences(adapters)
    multiplied_1_3 = differences[1] * differences[3]
    print(f"Product of 1-jolt and 3-jolt differences: {multiplied_1_3}")  # 2210

    distinct_chains = count_distinct_adapter_chains(adapters)
    print(
        f"Number of distinct ways to arrange the adapters: {distinct_chains}"
    )  # 7086739046912


if __name__ == "__main__":
    main()
