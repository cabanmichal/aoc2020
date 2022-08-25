#!/usr/bin/env python3
"""--- Day 18: Operation Order ---
https://adventofcode.com/2020/day/18"""

INPUT = "aoc2020_18_input.txt"


def process_right_value(
    right_value: int, operator: str | None, left_value: int | None
) -> tuple[str | None, int]:
    if operator is None:
        return operator, right_value

    if left_value is None:
        raise ValueError("Expression error: has operator but no value")

    if operator == "+":
        return None, left_value + right_value

    if operator == "*":
        return None, left_value * right_value

    raise ValueError(f"Unknown operator: {operator!r}")


def evaluate_no_precedence(tokens: list[str]) -> int:
    value = None
    operator = None

    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token in "+*":
            operator = token
        elif token.isdecimal():
            operator, value = process_right_value(int(token), operator, value)
        elif token == "(":
            brackets = 1
            start = index + 1
            while brackets:
                index += 1
                token = tokens[index]
                if token == "(":
                    brackets += 1
                elif token == ")":
                    brackets -= 1
            operator, value = process_right_value(
                evaluate_no_precedence(tokens[start:index]), operator, value
            )

        index += 1

    if value is None:
        raise ValueError("Expression evaluated to None")

    return value


def evaluate(expression: str) -> int:
    return evaluate_no_precedence([token for token in expression if token != " "])


def sum_of_expressions(expressions: list[str]) -> int:
    return sum(evaluate(expression) for expression in expressions)


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        expressions = infile.readlines()

    print(f"Sum part 1: {sum_of_expressions(expressions)}")  # 16332191652452


if __name__ == "__main__":
    main()
