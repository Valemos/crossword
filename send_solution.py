import sys
import time
from pathlib import Path

import parse
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from crossword.letter_grid import LetterGrid
from data_fetch.godville_browser import godville_browser
from data_fetch.human_mouse import HumanMouse
from data_fetch.human_typer import HumanTyper
from data_fetch.inputs_grid import InputsGrid
from data_fetch.human_random import *


with Path("output.txt").open('r') as fin:
    grid = LetterGrid.from_string(fin.read())

browser = godville_browser('news')

crossword_table: WebElement = browser.find_element(By.XPATH, "//table[@id='cross_tbl']/tbody")
cell_position = parse.compile("[{}][{}]")

crossword_cells = InputsGrid()
table_cells = crossword_table.find_elements(By.XPATH, "//input")
for cell in table_cells:
    position_parse = cell_position.parse(cell.get_attribute('name')[1:])
    if position_parse is None: continue
    x, y = position_parse
    crossword_cells.set_cell(int(x), int(y), cell)


crossword = grid.create_crossword()

mouse = HumanMouse(browser)
typer = HumanTyper(browser)


first_letter = crossword.words[0].letters[0]
last_cell = crossword_cells.get_cell(first_letter.x, first_letter.y)

# mouse.move_instant(last_cell)

for word in crossword.words:
    time.sleep(long_reaction_delay())

    for letter in word.letters:
        cell = crossword_cells.get_cell(letter.x, letter.y)
        if cell.get_attribute('value') == "":
            typer.type_once(cell, letter.character)
            time.sleep(0.1)
            # mouse.move(last_cell, cell)
            last_cell = cell

time.sleep(thinking_delay())

submit = crossword_table.find_element(By.XPATH, "//input[@id='crossword_submit']")
# mouse.move(last_cell, submit)
mouse.click(submit)

time.sleep(long_reaction_delay())
mouse.click(submit)
