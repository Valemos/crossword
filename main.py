from pathlib import Path

from crossword.crossword_bruteforce import CrosswordBruteforce
from crossword.unresolved_grid import LetterGrid

grid = LetterGrid.from_string("""
        ***и**еп*ик0бес*в*р****
        *000000000000000000000ч
        т000000000000000000000к
        о00д0000000*0000000у00*
        т00р0000000р0000000б00*
        р0***ы*** **р*з п*п*к0*
        е00*0000000х0000000и00м
        *00ь0000000у0000000*00е
        *0**п*ые****ьфст*и***0н
        *0000000000е0000000000*
        **остр***ц***т***ре*ко*
    """)
crossword = grid.create_crossword()

solver = CrosswordBruteforce()
solver.load_caches(Path("./categories"))


solved = solver.solve(crossword)

print(solved.to_grid_str())

print("\nSolved:")
for i, word in enumerate(solved.words):
    print(i, ":", word.get_pattern().replace("*", "."))
