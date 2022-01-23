from pathlib import Path

from crossword.crossword_bruteforce import CrosswordBruteforce
from crossword.unresolved_grid import LetterGrid

with Path("./input.txt").open('r') as fin:
    grid = LetterGrid.from_string(fin.read())

crossword = grid.create_crossword()

solver = CrosswordBruteforce()
solver.load_caches(Path("./categories"))


solved = solver.solve(crossword)

with Path("./output.txt").open('w') as fout:
    fout.write(solved.to_grid_str())

    fout.write("\n\nSolved:\n")
    for i, word in enumerate(solved.words):
        fout.write(f'{i}. {word.get_pattern().replace("*", ".")}\n')
