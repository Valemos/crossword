import sys
from pathlib import Path

from crossword.crossword_bruteforce import CrosswordBruteforce
from crossword.letter_grid import LetterGrid

with Path(sys.argv[1]).open('r') as fin:
    grid = LetterGrid.from_string(fin.read())

crossword = grid.create_crossword()

solver = CrosswordBruteforce()
solver.load_caches(Path("./categories"))
solved = solver.solve(crossword)

with Path(sys.argv[2]).open('w') as fout:
    fout.write(solved.grid.to_string('0'))
    print(solved.grid.to_string(' '))
