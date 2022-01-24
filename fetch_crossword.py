import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup
import parse

from crossword.letter_grid import LetterGrid
from data_fetch.godville_browser import godville_browser
from data_fetch.human_random import long_reaction_delay


_output_path = Path(sys.argv[1])
_response_save_path = Path("cw_response.txt")

use_cached = False
if len(sys.argv) > 2:
    use_cached = sys.argv[2] == "--cached"


def from_website():
    browser = godville_browser("news")
    source = browser.page_source
    time.sleep(long_reaction_delay())
    browser.close()
    return source


def to_file(text):
    with _response_save_path.open('w') as f:
        f.write(text)


if not use_cached:
    to_file(from_website())


with _response_save_path.open('r') as f:
    parsed_html = BeautifulSoup(f.read(), "html.parser")

crossword_table = parsed_html.find(id="cross_tbl").find("tbody")

grid = LetterGrid()

cell_position = parse.compile("[{}][{}]")

for row in crossword_table.find_all("tr"):
    for cell in row.find_all("td"):
        if "td_cell" not in cell.attrs["class"]:
            continue

        letter_input = cell.find("input")

        if "known" in cell.attrs["class"]:
            letter = letter_input.attrs["value"].lower()
        else:
            letter = '*'

        x, y = cell_position.parse(letter_input.attrs["name"][1:])

        grid.add_letter(letter, int(x), int(y))


with _output_path.open('w') as f:
    f.write(grid.to_string())
    print(grid.to_string(' '))
