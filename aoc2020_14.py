#!/usr/bin/env python3
"""--- Day 14: Docking Data ---
https://adventofcode.com/2020/day/14"""
import itertools
import re
from typing import Dict, List, NamedTuple, cast

INPUT = "aoc2020_14_input.txt"


class Instruction(NamedTuple):
    operation: str
    address: int | None
    value: str | int


class Program:
    pattern = re.compile(
        r"""
        (?P<operation>mem|mask)
        (\[(?P<address>\d+)\])?
        \ =\ (?P<value>[0-9X]+)
        """,
        re.VERBOSE,
    )

    def __init__(self) -> None:
        self._instructions: List[Instruction] = []
        self._memory: Dict[int, int] = {}
        self._mask: str = ""
        self._width = 36

    def load(self, filename: str) -> None:
        with open(filename, "rt", encoding="utf-8") as infile:
            for line in infile:
                line = line.strip()
                match = Program.pattern.match(line)
                if match is None:
                    raise ValueError(f"Can't parse instruction: {line!r}")

                operation = match.group("operation")
                address = match.group("address")
                value = match.group("value")

                if operation == "mask":
                    self._instructions.append(Instruction(operation, None, value))
                elif operation == "mem":
                    self._instructions.append(
                        Instruction(operation, int(address), int(value))
                    )
                else:
                    raise ValueError(f"Incorrect operation: {operation!r}")

    def execute_version_1(self) -> None:
        self._memory = {}
        for instruction in self._instructions:
            if instruction.operation == "mask":
                self._mask = cast(str, instruction.value)
            elif instruction.operation == "mem":
                self._memory[
                    cast(int, instruction.address)
                ] = self.apply_mask_version_1(cast(int, instruction.value))
            else:
                raise ValueError(f"Incorrect instruction: {instruction!r}")

    def apply_mask_version_1(self, value: int) -> int:
        bits = []
        for mask, bit in zip(self._mask, bin(value)[2:].zfill(self._width)):
            if mask == "X":
                bits.append(bit)
            else:
                bits.append(mask)
        return int("".join(bits), 2)

    def execute_version_2(self) -> None:
        self._memory = {}
        for instruction in self._instructions:
            if instruction.operation == "mask":
                self._mask = cast(str, instruction.value)
            elif instruction.operation == "mem":
                for address in self.apply_mask_version_2(
                    cast(int, instruction.address)
                ):
                    self._memory[address] = cast(int, instruction.value)
            else:
                raise ValueError(f"Incorrect instruction: {instruction!r}")

    def apply_mask_version_2(self, address: int) -> List[int]:
        bits = []
        floating_bits = []
        for idx, (mask, bit) in enumerate(
            zip(self._mask, bin(address)[2:].zfill(self._width))
        ):
            if mask == "X":
                floating_bits.append(idx)
                bits.append("X")
            elif mask == "1":
                bits.append(mask)
            else:
                bits.append(bit)

        combinations = itertools.product("01", repeat=len(floating_bits))
        addresses: List[int] = []
        for combination in combinations:
            for bit_idx, bit_value in zip(floating_bits, combination):
                bits[bit_idx] = bit_value
            addresses.append(int("".join(bits), 2))

        return addresses

    def dump_memory(self) -> Dict[int, int]:
        return self._memory.copy()


def main() -> None:
    program = Program()
    program.load(INPUT)

    program.execute_version_1()
    print(
        f"Memory values sum part 1: {sum(program.dump_memory().values())}"
    )  # 17481577045893

    program.execute_version_2()
    print(
        f"Memory values sum part 2: {sum(program.dump_memory().values())}"
    )  # 4160009892257


if __name__ == "__main__":
    main()
