from crossword.cell_type import CellType
from crossword.word_direction import WordDirection


class GridCell:
    def __init__(self, grid, letter, x, y):
        self._character = letter
        self._type = CellType.get_type(letter)
        self._x = x
        self._y = y
        self._grid = grid

    def __eq__(self, o) -> bool:
        return self.x == o.x and \
               self.y == o.y and \
               self.character == o.character

    def __hash__(self) -> int:
        return hash(self.position)

    def __str__(self):
        return f'{self._type.name} ({self._x}, {self._y}) : "{self._character}"'

    @staticmethod
    def wall(grid, x, y):
        return GridCell(grid, CellType.WALL.value, x, y)

    @property
    def character(self):
        return self._character

    @property
    def grid(self):
        return self._grid

    @character.setter
    def character(self, value):
        self._character = value
        self._type = CellType.get_type(value)

    @property
    def type(self) -> CellType:
        return self._type

    @property
    def position(self):
        return self._x, self._y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def top(self):
        return self._grid.get_cell(self._x, self._y - 1)

    @property
    def bottom(self):
        return self._grid.get_cell(self._x, self._y + 1)

    @property
    def left(self):
        return self._grid.get_cell(self._x - 1, self._y)

    @property
    def right(self):
        return self._grid.get_cell(self._x + 1, self._y)

    def back(self, direction: WordDirection):
        return self.left if direction == WordDirection.HORIZONTAL else self.top

    def forward(self, direction: WordDirection):
        return self.right if direction == WordDirection.HORIZONTAL else self.bottom

    def get_word_directions(self) -> list[WordDirection]:
        directions = []
        if self.left.type != CellType.WALL or self.right.type != CellType.WALL:
            directions.append(WordDirection.HORIZONTAL)

        if self.top.type != CellType.WALL or self.bottom.type != CellType.WALL:
            directions.append(WordDirection.VERTICAL)

        return directions

    def get_all_in_direction(self, direction):
        # get first letter
        current_letter = self
        while current_letter.type != CellType.WALL:
            current_letter = current_letter.back(direction)
        current_letter = current_letter.forward(direction)

        letters = []
        while current_letter.type != CellType.WALL:
            letters.append(current_letter)
            current_letter = current_letter.forward(direction)

        return letters
