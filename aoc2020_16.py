#!/usr/bin/env python3
"""--- Day 16: Ticket Translation ---
https://adventofcode.com/2020/day/16"""
import re
from itertools import chain

INPUT = "aoc2020_16_input.txt"
T_RULES = dict[str, list[tuple[int, int]]]


def load_input(input_file: str) -> tuple[list[str], list[str], list[str]]:
    with open(input_file, "rt", encoding="utf-8") as infile:
        content = infile.read()
    rules, my_ticket, other_tickets, *_ = content.split("\n\n")

    return (
        rules.splitlines(),
        my_ticket.splitlines()[1:],
        other_tickets.splitlines()[1:],
    )


def parse_rules(rules: list[str]) -> T_RULES:
    pattern = re.compile(r"([a-z ]+): (\d+-\d+) or (\d+-\d+)")
    parsed = {}
    for rule in rules:
        match = pattern.search(rule)
        if match is None:
            raise ValueError(f"Cannot parse rule: {rule!r}")
        name = match.group(1)
        ranges = []
        for range_ in match.groups()[1:]:
            start, end = range_.split("-")
            ranges.append((int(start), int(end)))

        parsed[str(name)] = ranges

    return parsed


def parse_tickets(tickets: list[str]) -> list[list[int]]:
    parsed = []
    for ticket in tickets:
        parsed.append([int(number) for number in ticket.split(",")])

    return parsed


def invalid_ticket_numbers(ticket: list[int], rules: T_RULES) -> list[int]:
    invalid_numbers = []
    for number in ticket:
        for start, end in chain.from_iterable(rules.values()):
            if start <= number <= end:
                break
        else:
            invalid_numbers.append(number)
    return invalid_numbers


def is_ticket_valid(ticket: list[int], rules: T_RULES) -> bool:
    return not invalid_ticket_numbers(ticket, rules)


def sum_of_invalid_values(tickets: list[list[int]], rules: T_RULES) -> int:
    error_rate = 0
    for ticket in tickets:
        error_rate += sum(invalid_ticket_numbers(ticket, rules))
    return error_rate


def fields_in_order(tickets: list[list[int]], rules: T_RULES) -> list[str]:
    tickets = [ticket for ticket in tickets if is_ticket_valid(ticket, rules)]
    all_fields = set(rules)
    ordered_fields: list[set[str]] = [set(all_fields) for _ in rules]

    for ticket in tickets:
        for idx, value in enumerate(ticket):
            possible_fields = set()
            for field, ranges in rules.items():
                for start, end in ranges:
                    if start <= value <= end:
                        possible_fields.add(field)
                        break
            ordered_fields[idx].intersection_update(possible_fields)

    while all_fields:
        for i, fields in enumerate(ordered_fields):
            if len(fields) != 1:
                continue
            field, *_ = fields
            if field not in all_fields:
                continue
            all_fields.discard(field)

            for j, fields in enumerate(ordered_fields):
                if i != j:
                    fields.discard(field)

    return [field.pop() for field in ordered_fields]


def product_of_departure_fields(ticket: list[int], fields: list[str]) -> int:
    product = 1
    for value, field in zip(ticket, fields):
        if field.startswith("departure"):
            product *= value

    return product


def main() -> None:
    unparsed_rules, unparsed_my_tickets, unparsed_tickets = load_input(INPUT)
    rules = parse_rules(unparsed_rules)
    my_tickets = parse_tickets(unparsed_my_tickets)
    other_tickets = parse_tickets(unparsed_tickets)

    answer = sum_of_invalid_values(other_tickets, rules)
    print(f"Ticket scanning error rate: {answer}")  # 25895

    answer = product_of_departure_fields(
        my_tickets[0], fields_in_order(my_tickets + other_tickets, rules)
    )
    print(f"Product of departure fields: {answer}")  # 5865723727753


if __name__ == "__main__":
    main()
