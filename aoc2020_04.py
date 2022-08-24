#!/usr/bin/env python3
"""--- Day 4: Passport Processing ---
https://adventofcode.com/2020/day/4"""
import re
from typing import Dict, List

INPUT = "aoc2020_04_input.txt"
PASSPORT_FIELDS = {
    "byr": "Birth Year",
    "iyr": "Issue Year",
    "eyr": "Expiration Year",
    "hgt": "Height",
    "hcl": "Hair Color",
    "ecl": "Eye Color",
    "pid": "Passport ID",
    "cid": "Country ID",
}
OPTIONAL_FIELD = "cid"


def is_valid_passport(document: Dict[str, str]) -> bool:
    diff = PASSPORT_FIELDS.keys() - document.keys()
    return not diff or len(diff) == 1 and OPTIONAL_FIELD in diff


def _number_valid(number_string: str, low: int, high: int) -> bool:
    try:
        number = int(number_string)
    except ValueError:
        return False

    return low <= number <= high


def byr_valid(byr: str) -> bool:
    return _number_valid(byr, 1920, 2002)


def iyr_valid(iyr: str) -> bool:
    return _number_valid(iyr, 2010, 2020)


def eyr_valid(eyr: str) -> bool:
    return _number_valid(eyr, 2020, 2030)


def hgt_valid(hgt: str) -> bool:
    value = hgt[:-2]
    unit = hgt[-2:]
    if unit == "cm":
        return _number_valid(value, 150, 193)
    if unit == "in":
        return _number_valid(value, 59, 76)
    return False


def hcl_valid(hcl: str) -> bool:
    return re.fullmatch(r"#[0-9a-f]{6}", hcl) is not None


def ecl_valid(ecl: str) -> bool:
    return re.fullmatch(r"amb|blu|brn|gry|grn|hzl|oth", ecl) is not None


def pid_valid(pid: str) -> bool:
    return len(pid) == 9 and pid.isnumeric()


def is_valid_passport_strict(document: Dict[str, str]) -> bool:
    return (
        is_valid_passport(document)
        and byr_valid(document["byr"])
        and iyr_valid(document["iyr"])
        and eyr_valid(document["eyr"])
        and hgt_valid(document["hgt"])
        and hcl_valid(document["hcl"])
        and ecl_valid(document["ecl"])
        and pid_valid(document["pid"])
    )


def parse_input(file_name: str) -> List[Dict[str, str]]:
    documents = []
    document: Dict[str, str] = {}

    with open(file_name, "rt", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if not line and document:
                documents.append(document)
                document = {}
                continue

            document.update(
                {
                    key: value
                    for key, value in (item.split(":") for item in line.split())
                }
            )

        if document:
            documents.append(document)

    return documents


def main() -> None:
    valid_count_1 = 0
    valid_count_2 = 0
    for document in parse_input(INPUT):
        if is_valid_passport(document):
            valid_count_1 += 1
        if is_valid_passport_strict(document):
            valid_count_2 += 1

    print(f"Valid documents: {valid_count_1} / {valid_count_2}")  # 235 / 194


if __name__ == "__main__":
    main()
