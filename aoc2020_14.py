#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/14"""
import re
from typing import Dict, List

INPUT = "aoc2020_14_input.txt"


class Program:
    def __init__(self) -> None:
        self._instructions: List[str] = []
        self._memory: Dict[int, int] = {}
        self._mask: str = ""
        self._width = 36

    def load(self, filename: str) -> None:
        with open(filename, "rt", encoding="utf-8") as infile:
            self._instructions = infile.readlines()

    def execute(self) -> None:
        self._memory = {}
        for instruction in self._instructions:
            if instruction.startswith("mask"):
                self._mask = instruction.strip().split(" = ")[1]
            elif instruction.startswith("mem"):
                match = re.search(r"(\d+).+?(\d+)", instruction)
                if match is None:
                    raise ValueError(f"Can't parse instruction: {instruction!r}")
                address, value, *_ = match.groups()
                self._memory[int(address)] = self.apply_mask(int(value))
            else:
                raise ValueError(f"Incorrect instruction: {instruction!r}")

    def dump_memory(self) -> Dict[int, int]:
        return self._memory.copy()

    def apply_mask(self, value: int) -> int:
        bits = []
        for mask, bit in zip(self._mask, bin(value)[2:].zfill(self._width)):
            if mask == "X":
                bits.append(bit)
            else:
                bits.append(mask)
        return int("".join(bits), 2)


def main() -> None:
    program = Program()
    program.load(INPUT)
    program.execute()
    print(sum(program.dump_memory().values()))  # 17481577045893


if __name__ == "__main__":
    main()
