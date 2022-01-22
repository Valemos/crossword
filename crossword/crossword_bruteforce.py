from copy import deepcopy
from pathlib import Path
from typing import Optional

import yaml

from crossword.cell_type import CellType
from crossword.crossword import Crossword
from crossword.word import Word
from data_fetch.godville_request import search_godville_crossword


class SolutionError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CrosswordBruteforce:

    default_name = "default"
    search_cache_name = "search_cache"

    def __init__(self, solutions=None):
        self._category_solutions: dict[str, list[str]] = solutions if solutions is not None else {}
        self._file_path = Path()

    def load_caches(self, path: Path):
        for file in path.glob("*.txt"):
            with file.open('r') as fin:
                self._category_solutions[file.stem] = [line.strip() for line in fin.readlines()]
                self._file_path = path

    def solve(self, crossword: Crossword) -> Optional[Crossword]:
        crossword_copy = deepcopy(crossword)
        for word in crossword_copy.unsolved_words:
            for solution in self._find_matches(word):
                word.set_letters(solution)
                crossword_copy = self.solve(crossword_copy)
                if crossword_copy is not None:
                    break

        return crossword_copy

    @staticmethod
    def tokenize_answer(string: str):
        return string.strip('\t\n (@)').lower()

    def _find_matches(self, word: Word):
        for value in self._category_solutions[self.default_name]:
            if word.is_pattern_matches(value):
                yield value

        for value in self._category_solutions[self.search_cache_name]:
            if word.is_pattern_matches(value):
                yield value

        # last resort - search online database
        query = word.get_pattern().replace(CellType.VACANT.value, '.')
        found_answers = search_godville_crossword(query)
        found_answers = list(map(self.tokenize_answer, found_answers))
        self._save_found_answers(found_answers)

        for value in found_answers:
            if word.is_pattern_matches(value):
                yield value

    def _save_found_answers(self, found_answers):

        append_answers = []
        for answer in found_answers:
            if answer not in self._category_solutions[self.search_cache_name]:
                append_answers.append(answer)
                self._category_solutions[self.search_cache_name].append(answer)

        with (self._file_path / self.search_cache_name).with_suffix('.txt').open('a') as fout:
            for answer in append_answers:
                fout.write(answer)
                fout.write('\n')
