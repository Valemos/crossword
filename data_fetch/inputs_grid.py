from crossword.extendable_grid import ExtendableGrid


class VacantPlaceMock:
    pass


class InputsGrid(ExtendableGrid):

    def __init__(self):
        super().__init__()

    def create_empty_cell(self, x, y):
        return VacantPlaceMock


