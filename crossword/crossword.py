from .cell_type import CellType
from .word import Word


class Crossword:
    def __init__(self):
        self._words: list[Word] = []
        self._position_to_words: dict[tuple[int, int], list[Word]] = {}

    def add_word(self, word: Word):
        self._words.append(word)

        for letter in word.letters:
            position = letter.position
            words = self._position_to_words.get(position, [])
            words.append(word)
            self._position_to_words[position] = words

    @property
    def words(self):
        return self._words

    @property
    def unsolved_words(self):
        return (word for word in self._words if not word.is_solved())

    def get_cell_words(self, x, y):
        position = (x, y)
        if position in self._position_to_words:
            return self._position_to_words[position]
        raise ValueError("no word for letter found")

    def to_grid_str(self):
        grid = self._words[0].letters[0].grid
        return '\n'.join((''.join(
            grid.get_cell(x, y).character
            for x in range(grid.x_size))
            for y in range(grid.y_size))
        ).replace(CellType.WALL.value, ' ')
