import pytest

from crossword.unresolved_grid import LetterGrid


@pytest.fixture()
def merged():
    return "**\n" \
           "**"


@pytest.fixture()
def square():
    return "***\n" \
           "*0*\n" \
           "***"


@pytest.fixture()
def star():
    return "0*0\n" \
           "***\n" \
           "0*0"


@pytest.fixture()
def t_shape():
    return "***\n" \
           "0*0\n" \
           "0*0"


def words_test(crossword, test_words):
    assert len(crossword.words) == len(test_words)
    assert all((word.letters in test_words for word in crossword.words))


def test_star(star):
    grid = LetterGrid.from_string(star)
    crossword = grid.create_crossword()
    words_test(crossword, [
        [grid.get_cell(1, 0), grid.get_cell(1, 1), grid.get_cell(1, 2)],
        [grid.get_cell(0, 1), grid.get_cell(1, 1), grid.get_cell(2, 1)]
    ])


def test_merged(merged):
    grid = LetterGrid.from_string(merged)
    crossword = grid.create_crossword()

    words_test(crossword, [
        [grid.get_cell(0, 0), grid.get_cell(0, 1)],
        [grid.get_cell(0, 0), grid.get_cell(1, 0)],
        [grid.get_cell(1, 0), grid.get_cell(1, 1)],
        [grid.get_cell(0, 1), grid.get_cell(1, 1)]
    ])


def test_square(square):
    grid = LetterGrid.from_string(square)
    crossword = grid.create_crossword()
    words_test(crossword, [
        [grid.get_cell(0, 0), grid.get_cell(0, 1), grid.get_cell(0, 2)],
        [grid.get_cell(0, 0), grid.get_cell(1, 0), grid.get_cell(2, 0)],
        [grid.get_cell(0, 2), grid.get_cell(1, 2), grid.get_cell(2, 2)],
        [grid.get_cell(2, 0), grid.get_cell(2, 1), grid.get_cell(2, 2)],
    ])


def test_t_shape(t_shape):
    grid = LetterGrid.from_string(t_shape)
    crossword = grid.create_crossword()
    words_test(crossword, [
        [grid.get_cell(0, 0), grid.get_cell(1, 0), grid.get_cell(2, 0)],
        [grid.get_cell(1, 0), grid.get_cell(1, 1), grid.get_cell(1, 2)],
    ])
