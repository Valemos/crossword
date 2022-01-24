from abc import abstractmethod

from crossword.grid_cell import GridCell


class ExtendableGrid:
    def __init__(self):
        self._grid: list[list[object]] = []

    @property
    def x_size(self):
        return len(self._grid)

    @property
    def y_size(self):
        if self.x_size > 0:
            return len(self._grid[0])
        else:
            return 0

    @abstractmethod
    def create_empty_cell(self, x, y):
        pass

    def get_cell(self, x, y):
        if self.is_inside(x, y):
            return self._grid[x][y]
        else:
            return self.create_empty_cell(x, y)

    def set_cell(self, x, y, cell):
        self.extend_to_fit(x, y)
        self._grid[x][y] = cell

    def is_inside(self, x, y):
        return 0 <= x < self.x_size and \
               0 <= y < self.y_size

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
        self._grid.append([self.create_empty_cell(x, y) for y in range(self.y_size)])

    def _append_y_dimension(self):
        y = self.y_size
        for x, column in enumerate(self._grid):
            column.append(GridCell.wall(self, x, y))
