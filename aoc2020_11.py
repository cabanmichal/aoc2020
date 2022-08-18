#!/usr/bin/env python3
"""https://adventofcode.com/2020/day/11"""
from collections import Counter
from typing import Dict, Iterator, List, Literal, Tuple

INPUT = "aoc2020_11_input.txt"
EMPTY = "L"
OCCUPIED = "#"
FLOOR = "."


class WaitingArea:
    def __init__(self, seat_layout: List[List[str]]) -> None:
        self.seat_layout = seat_layout
        self.width = len(seat_layout[0])
        self.height = len(self.seat_layout)

    def make_round(
        self, method: Literal["adjacent", "visible"], tolerance: int
    ) -> bool:
        seat_layout = [[c for c in r] for r in self.seat_layout]
        layout_changed = False

        for row in range(self.height):
            for column in range(self.width):
                if method == "adjacent":
                    counter = self._adjacent_counter(row, column)
                elif method == "visible":
                    counter = self._visible_counter(row, column)
                else:
                    raise ValueError(f"Incorrect method specified: {method!r}")

                seat_state = self.seat_layout[row][column]
                if seat_state == EMPTY and not counter.get(OCCUPIED, 0):
                    seat_layout[row][column] = OCCUPIED
                    layout_changed = True
                elif seat_state == OCCUPIED and counter.get(OCCUPIED, 0) >= tolerance:
                    seat_layout[row][column] = EMPTY
                    layout_changed = True

        self.seat_layout = seat_layout

        return layout_changed

    @property
    def occupied_seats(self) -> int:
        counter = 0
        for row in self.seat_layout:
            for item in row:
                if item == OCCUPIED:
                    counter += 1
        return counter

    def _adjacent_coordinates(self, row: int, column: int) -> Iterator[Tuple[int, int]]:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = column + dc
                if 0 <= r < self.height and 0 <= c < self.width:
                    yield r, c

    def _adjacent_counter(self, row: int, column: int) -> Dict[str, int]:
        return Counter(
            self.seat_layout[r][c] for r, c in self._adjacent_coordinates(row, column)
        )

    def _visible_coordinates(
        self, row: int, column: int, direction: Tuple[int, int]
    ) -> Iterator[Tuple[int, int]]:
        dr, dc = direction
        while True:
            row += dr
            column += dc
            if 0 <= row < self.height and 0 <= column < self.width:
                yield row, column
            else:
                return

    def _visible_counter(self, row: int, column: int) -> Dict[str, int]:
        counter: Dict[str, int] = Counter()
        for direction in [
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ]:
            for r, c in self._visible_coordinates(row, column, direction):
                if self.seat_layout[r][c] in [EMPTY, OCCUPIED]:
                    counter[self.seat_layout[r][c]] += 1
                    break
        return counter

    def __str__(self) -> str:
        return "\n" + "\n".join("".join(row) for row in self.seat_layout) + "\n"


def occupied_seats_method_1(seat_layout: List[List[str]]) -> int:
    waiting_area = WaitingArea(seat_layout)
    seats_changed = waiting_area.make_round("adjacent", tolerance=4)
    while seats_changed:
        seats_changed = waiting_area.make_round("adjacent", tolerance=4)
    return waiting_area.occupied_seats


def occupied_seats_method_2(seat_layout: List[List[str]]) -> int:
    waiting_area = WaitingArea(seat_layout)
    seats_changed = waiting_area.make_round("visible", tolerance=5)
    while seats_changed:
        seats_changed = waiting_area.make_round("visible", tolerance=5)
    return waiting_area.occupied_seats


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        seat_layout = [list(line.strip()) for line in infile]

    print(
        f"Number of occupied seats part 1: {occupied_seats_method_1(seat_layout)}"
    )  # 2178
    print(
        f"Number of occupied seats part 2: {occupied_seats_method_2(seat_layout)}"
    )  # 1978


if __name__ == "__main__":
    main()
