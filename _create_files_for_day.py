#!/usr/bin/env python3
import sys

YEAR = 2020
INPUT_TEMPLATE = "aoc{}_{:02}_input.txt"
SCRIPT_TEMPLATE = "aoc{}_{:02}.py"


def main() -> None:
    day_number = int(sys.argv[1])
    input_file_name = INPUT_TEMPLATE.format(YEAR, day_number)
    script_file_name = SCRIPT_TEMPLATE.format(YEAR, day_number)

    with open(input_file_name, "w"):
        pass

    with open(script_file_name, "w", encoding="utf-8") as scriptifle:
        scriptifle.write(f"\n\nINPUT = {input_file_name!r}\n\n\n")
        scriptifle.write("def main() -> None:\n    pass\n\n\n")
        scriptifle.write('if __name__ == "__main__":\n    main()\n')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} day_number")
        sys.exit(1)

    main()
