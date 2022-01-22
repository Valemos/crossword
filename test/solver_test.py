import pytest

from crossword.crossword_bruteforce import CrosswordBruteforce
from crossword.unresolved_grid import LetterGrid
from crossword.word import Word


def test_patterns():
    assert not Word.from_string("hello").is_pattern_matches("hel")
    assert not Word.from_string("****").is_pattern_matches("hello")
    assert not Word.from_string("12345").is_pattern_matches("hello")
    assert Word.from_string("h**lo").is_pattern_matches("hello")
    assert Word.from_string("*****").is_pattern_matches("hello")


def test_solver():
    grid = LetterGrid.from_string("""
        *a**e
        000o0
        000*0
        """)
    crossword = grid.create_crossword()

    expected = [
        "maybe",
        "boy"
    ]
    solver = CrosswordBruteforce({"": expected})

    solved = solver.solve(crossword)

    assert all(word.get_pattern() in expected for word in solved.words)
