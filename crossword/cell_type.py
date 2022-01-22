import enum


class CellType(enum.Enum):
    WALL = '0'
    VACANT = '*'
    KNOWN = 0

    @staticmethod
    def get_type(letter):
        if CellType.WALL.value == letter:
            return CellType.WALL
        elif CellType.VACANT.value == letter:
            return CellType.VACANT
        else:
            return CellType.KNOWN
