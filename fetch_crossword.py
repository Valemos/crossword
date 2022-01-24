import time
from pathlib import Path

from bs4 import BeautifulSoup
import requests
import json
import parse

from selenium.webdriver import Firefox as Browser
from selenium.webdriver.firefox.options import Options

from crossword.letter_grid import LetterGrid
from data_fetch.human_random_time import long_reaction_delay


_output_path = Path("input.txt")
_response_save_path = Path("cw_response.txt")
_cookies_path = Path("cookies.json")


def load_cookies(browser):
    with _cookies_path.open("r") as fin:
        cookies = json.load(fin)

    for cookie in cookies:
        browser.add_cookie(cookie)


def from_website():
    options = Options()
    options.binary = "/home/anton/tools/firefox/firefox"

    browser = Browser(options=options)
    browser.get("https://godville.net/news")
    load_cookies(browser)
    browser.refresh()
    source = browser.page_source
    time.sleep(long_reaction_delay())
    browser.close()
    return source


def to_file(text):
    with _response_save_path.open('w') as f:
        f.write(text)


def from_file():
    with _response_save_path.open('r') as f:
        return f.read()


# to_file(from_website())

parsed_html = BeautifulSoup(from_file(), "html.parser")
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
