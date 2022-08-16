#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/8"""
from dataclasses import dataclass
from typing import List

INPUT = "aoc2020_08_input.txt"


@dataclass
class Instruction:
    operation: str
    value: int


class Program:
    def __init__(self) -> None:
        self.instructions: List[Instruction] = []
        self.counter: List[int] = []
        self.pointer = 0
        self.accumulator = 0
        self.has_error = False

    def _reset(self) -> None:
        self.counter = [0] * len(self.instructions)
        self.pointer = 0
        self.accumulator = 0
        self.has_error = False

    def load(self, input_file: str) -> None:
        with open(input_file, "rt", encoding="utf-8") as infile:
            for line in infile:
                operation, string_value, *_ = line.strip().split()
                self.instructions.append(Instruction(operation, int(string_value)))
        self._reset()

    def execute(self) -> None:
        self._reset()
        while self.pointer < len(self.instructions):
            if self.counter[self.pointer] > 0:
                self.has_error = True
                return

            self.counter[self.pointer] += 1
            instruction = self.instructions[self.pointer]
            if instruction.operation == "nop":
                self.pointer += 1
            elif instruction.operation == "acc":
                self.accumulator += instruction.value
                self.pointer += 1
            elif instruction.operation == "jmp":
                self.pointer += instruction.value
            else:
                raise ValueError(f"Incorrect operation: {instruction.operation!r}")

    def repair(self) -> None:
        self.execute()
        if not self.has_error:
            return

        for instruction in self.instructions:
            if instruction.operation == "acc":
                continue

            original_operation = instruction.operation
            if original_operation == "nop":
                instruction.operation = "jmp"
            elif original_operation == "jmp":
                instruction.operation = "nop"
            else:
                raise ValueError(f"Incorrect operation: {original_operation!r}")

            self.execute()
            if not self.has_error:
                return

            instruction.operation = original_operation

        if self.has_error:
            raise RuntimeError("Program unrepairable")


def main() -> None:
    program = Program()
    program.load(INPUT)
    program.execute()
    print(f"Accumulator of broken program: {program.accumulator}")  # 1766
    program.repair()
    print(f"Accumulator of fixed program: {program.accumulator}")  # 1639


if __name__ == "__main__":
    main()
