import dataclasses

from crossword.cell_type import CellType
from crossword.grid_cell import GridCell
from crossword.word_direction import WordDirection


@dataclasses.dataclass
class Word:
    letters: list[GridCell]
    direction: WordDirection

    @classmethod
    def from_string(cls, string: str):
        letters = [GridCell(None, char, 0, i) for i, char in enumerate(string)]
        return cls(letters, WordDirection.HORIZONTAL)

    def __str__(self):
        return f"{self.get_pattern()} [{self.direction.name}]"

    @property
    def grid(self):
        if len(self.letters) > 0:
            return self.letters[0].grid
        return None

    def get_pattern(self):
        return ''.join(letter.character for letter in self.letters)

    def set_letters(self, string: str):
        for letter_cell, character in zip(self.letters, string):
            letter_cell.character = character

    def is_solved(self):
        return not any((letter.character == CellType.VACANT.value for letter in self.letters))

    def is_pattern_matches(self, string: str) -> bool:
        pattern = self.get_pattern()
        if len(pattern) != len(string):
            return False

        for i, (pattern_letter, compare_letter) in enumerate(zip(pattern, string)):
            if pattern_letter != CellType.VACANT.value:
                if compare_letter != pattern_letter:
                    return False

        return True
