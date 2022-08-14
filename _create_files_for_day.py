#!/usr/bin/env python3
import sys

YEAR = 2020
INPUT_TEMPLATE = "aoc{}_{:02}_input.txt"
SCRIPT_TEMPLATE = "aoc{}_{:02}.py"
URL_TEMPLATE = "https://adventofcode.com/{}/day/{}"


def main() -> None:
    day_number = int(sys.argv[1])
    url = URL_TEMPLATE.format(YEAR, day_number)
    input_file_name = INPUT_TEMPLATE.format(YEAR, day_number)
    script_file_name = SCRIPT_TEMPLATE.format(YEAR, day_number)

    with open(input_file_name, "w"):
        pass

    with open(script_file_name, "w", encoding="utf-8") as scriptfile:
        scriptfile.write(
            "\n".join(
                [
                    "#!/usr/bin/env python3",
                    f'"""{url}"""',
                    "\n",
                    f"INPUT = {input_file_name!r}",
                    "\n",
                    "def main() -> None:",
                    "    pass",
                    "\n",
                    'if __name__ == "__main__":',
                    "    main()",
                ]
            )
            + "\n"
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} day_number")
        sys.exit(1)

    main()
