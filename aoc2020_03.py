from typing import Tuple, Iterable
import math


INPUT = "aoc2020_03_input.txt"
TREE = "#"
SLOPE = (3, 1)
SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]


def is_tree(x_coordinate: int, tree_row: str) -> bool:
    idx = x_coordinate % len(tree_row)
    return tree_row[idx] == TREE


def count_trees_in_way(terrain_map_lines: Iterable[str], slope: Tuple[int, int]) -> int:
    count = 0
    x_coordinate = 0
    dx, dy = slope

    if dy <= 0 or dx <= 0:
        raise ValueError(f"Slope must be higher than 0 ({slope})")

    for idx, line in enumerate(terrain_map_lines):
        if idx == 0:
            continue

        if idx % dy == 0:
            x_coordinate += dx
            if is_tree(x_coordinate, line.strip()):
                count += 1

    return count


def main() -> None:
    trees = []
    with open(INPUT, "rt", encoding="utf-8") as infile:
        terrain_map_lines = infile.readlines()

    for slope in SLOPES:
        count = count_trees_in_way(terrain_map_lines, slope)
        trees.append(count)
        if slope == SLOPE:
            print(f"Encountered trees: {count}")

    product = math.prod(trees)
    print(f"Product of trees for slopes: {product} ({trees})")


if __name__ == "__main__":
    main()
