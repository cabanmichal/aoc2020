#!/usr/bin/env python3
import sys
import urllib.request
from html.parser import HTMLParser

YEAR = 2020
INPUT_TEMPLATE = "aoc{}_{:02}_input.txt"
SCRIPT_TEMPLATE = "aoc{}_{:02}.py"
URL_TEMPLATE = "https://adventofcode.com/{}/day/{}"


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_main = False
        self.in_article = False
        self.in_h2 = False
        self.heading: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "main":
            self.in_main = True
        elif tag == "article":
            self.in_article = True
        elif tag == "h2":
            self.in_h2 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "main":
            self.in_main = False
        elif tag == "article":
            self.in_article = False
        elif tag == "h2":
            self.in_h2 = False

    def handle_data(self, data: str) -> None:
        if self.in_main and self.in_article and self.in_h2 and self.heading is None:
            self.heading = data.strip()


def get_html_content(url: str) -> str:
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode("utf-8")


def get_heading(url: str) -> str | None:
    parser = HeadingParser()
    parser.feed(get_html_content(url))
    return parser.heading


def main() -> None:
    day_number = int(sys.argv[1])
    url = URL_TEMPLATE.format(YEAR, day_number)
    heading = get_heading(url)
    input_file_name = INPUT_TEMPLATE.format(YEAR, day_number)
    script_file_name = SCRIPT_TEMPLATE.format(YEAR, day_number)

    with open(input_file_name, "w"):
        pass

    with open(script_file_name, "w", encoding="utf-8") as scriptfile:
        scriptfile.write(
            "\n".join(
                [
                    "#!/usr/bin/env python3",
                    f'"""{heading}\n{url}"""',
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
