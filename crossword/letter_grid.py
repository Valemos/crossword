from .crossword import Crossword
from .extendable_grid import ExtendableGrid
from .grid_cell import GridCell
from .cell_type import CellType
from .word import Word


class LetterGrid(ExtendableGrid):
    """
    x axis positive left
    y axis positive down

         col1 col2
    row1 0,0  1,0
    row2 0,1  1,1
    """

    def __init__(self):
        super().__init__()
        self._letter_cells: list[GridCell] = []

    @staticmethod
    def from_string(string):
        grid = LetterGrid()
        for row_i, row in enumerate(string.strip().split('\n')):
            for col_i, letter in enumerate(row.strip()):
                grid.add_letter(letter, col_i, row_i)

        return grid

    def get_cell(self, x, y) -> GridCell:
        return super().get_cell(x, y)

    def to_string(self, wall_value='0'):
        return '\n'.join((''.join(
            self.get_cell(x, y).character
            for x in range(self.x_size))
            for y in range(self.y_size))
        ).replace(CellType.WALL.value, wall_value)

    def create_crossword(self) -> Crossword:
        crossword = Crossword()

        available_cells = {cell: cell.get_word_directions() for cell in self._letter_cells}

        while len(available_cells) > 0:
            cell, directions = next(iter(available_cells.items()))
            if len(directions) == 0:
                del available_cells[cell]
                continue

            current_direction = directions.pop()
            letters = cell.get_all_in_direction(current_direction)
            for letter in letters:
                if current_direction in available_cells[letter]:
                    available_cells[letter].remove(current_direction)

            crossword.add_word(Word(letters, current_direction))

        return crossword

    def create_empty_cell(self, x, y):
        return GridCell.wall(self, x, y)

    def add_letter(self, letter, x, y):
        """cannot add cells before x = 0, y = 0 only builds forwards"""

        cell = GridCell(self, letter, x, y)
        self.set_cell(x, y, cell)

        if cell.type != CellType.WALL:
            self._letter_cells.append(cell)
