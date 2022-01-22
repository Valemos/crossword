from .crossword import Crossword
from .grid_cell import GridCell
from .cell_type import CellType
from .word import Word


class LetterGrid:
    """
    x axis positive left
    y axis positive down

         col1 col2
    row1 0,0  1,0
    row2 0,1  1,1
    """
    def __init__(self):
        self._grid: list[list[GridCell]] = []
        self._letter_cells: list[GridCell] = []

    @staticmethod
    def from_string(string):
        grid = LetterGrid()
        for row_i, row in enumerate(string.strip().split('\n')):
            for col_i, letter in enumerate(row.strip()):
                grid.add_cell(GridCell(grid, letter, col_i, row_i))

        return grid

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

    def is_inside(self, x, y):
        return 0 <= x < self.x_size and \
               0 <= y < self.y_size

    @property
    def x_size(self):
        return len(self._grid)

    @property
    def y_size(self):
        if self.x_size > 0:
            return len(self._grid[0])
        else:
            return 0

    def get_cell(self, x, y):
        if self.is_inside(x, y):
            return self._grid[x][y]
        else:
            return GridCell.wall(self, x, y)

    def add_cell(self, cell: GridCell):
        """cannot add cells before x = 0, y = 0 only builds forwards"""
        self.extend_to_fit(cell.x, cell.y)
        self._grid[cell.x][cell.y] = cell

        if cell.type != CellType.WALL:
            self._letter_cells.append(cell)

    def extend_to_fit(self, x, y):
        if self.is_inside(x, y):
            return

        x_extra = max(0, x + 1 - self.x_size)
        y_extra = max(0, y + 1 - self.y_size)

        for _ in range(x_extra):
            self._append_x_dimension()

        for _ in range(y_extra):
            self._append_y_dimension()

    def _append_x_dimension(self):
        x = self.x_size
        self._grid.append([GridCell.wall(self, x, y) for y in range(self.y_size)])

    def _append_y_dimension(self):
        y = self.y_size
        for x, column in enumerate(self._grid):
            column.append(GridCell.wall(self, x, y))
