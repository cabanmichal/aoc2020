#!/usr/bin/env python3
"""--- Day 18: Operation Order ---
https://adventofcode.com/2020/day/18"""

INPUT = "aoc2020_18_input.txt"


def tokenize(expression: str) -> list[str]:
    return [token for token in expression if token != " "]


def find_group_end(tokens: list[str], group_start: int) -> int:
    index = group_start
    brackets = 1
    while brackets:
        index += 1
        if index >= len(tokens):
            break

        token = tokens[index]
        if token == "(":
            brackets += 1
        elif token == ")":
            brackets -= 1

    if brackets:
        raise ValueError("Parentheses mismatch")

    return index


def process_value_no_precedence(
    left_value: int | None, operator: str | None, right_value: int
) -> int:
    if left_value is None:
        return right_value

    if operator == "+":
        return left_value + right_value

    if operator == "*":
        return left_value * right_value

    raise ValueError(f"Unknown operator: {operator!r}")


def evaluate_no_precedence(tokens: list[str]) -> int:
    operator = None
    value = None
    index = 0

    while index < len(tokens):
        token = tokens[index]

        if token in "+*":
            operator = token
        elif token.isdecimal():
            value = process_value_no_precedence(value, operator, int(token))
        elif token == "(":
            start = index + 1
            index = find_group_end(tokens, index)
            value = process_value_no_precedence(
                value, operator, evaluate_no_precedence(tokens[start:index])
            )

        index += 1

    if value is None:
        raise ValueError("Expression evaluated to None")

    return value


def process_value_precedence(
    left_value: int | None,
    current_operator: str | None,
    right_value: int,
    precedence_operator: str,
) -> tuple[int, list[str]]:
    tokens: list[str] = []
    if left_value is None:
        return right_value, tokens

    if current_operator is None:
        raise ValueError(f"Unknown operator: {current_operator!r}")

    if current_operator == precedence_operator:
        if precedence_operator == "+":
            return left_value + right_value, tokens
        if precedence_operator == "*":
            return left_value * right_value, tokens
        raise ValueError(f"Unknown operator: {current_operator!r}")
    else:
        tokens.append(str(left_value))
        tokens.append(current_operator)
        return right_value, tokens


def evaluate_with_precedence(tokens: list[str], operators: list[str]) -> int:
    for precedence_operator in operators:
        current_operator = None
        value = None
        new_tokens: list[str] = []
        index = 0

        while index < len(tokens):
            token = tokens[index]

            if token.isdecimal():
                value, processed_tokens = process_value_precedence(
                    value, current_operator, int(token), precedence_operator
                )
                new_tokens.extend(processed_tokens)
            elif token in operators:
                current_operator = token
            elif token == "(":
                start = index + 1
                index = find_group_end(tokens, index)
                value, processed_tokens = process_value_precedence(
                    value,
                    current_operator,
                    evaluate_with_precedence(tokens[start:index], operators),
                    precedence_operator,
                )
                new_tokens.extend(processed_tokens)

            index += 1

        new_tokens.append(str(value))
        tokens = new_tokens

    return int(tokens.pop())


def evaluate(expression: str, with_precedence: bool) -> int:
    tokens = tokenize(expression)
    if with_precedence:
        return evaluate_with_precedence(tokens, list("+*"))
    return evaluate_no_precedence(tokens)


def sum_of_expressions(expressions: list[str], with_precedence: bool) -> int:
    return sum(evaluate(expression, with_precedence) for expression in expressions)


def main() -> None:
    with open(INPUT, "rt", encoding="utf-8") as infile:
        expressions = [line.strip() for line in infile]

    answer = sum_of_expressions(expressions, with_precedence=False)
    print(f"Sum with no precedence: {answer}")  # 16332191652452

    answer = sum_of_expressions(expressions, with_precedence=True)
    print(f"Sum with addition precedence: {answer}")  # 351175492232654


if __name__ == "__main__":
    main()
