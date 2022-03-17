from dataclasses import dataclass
from typing import Tuple
from constants import FACE, EDGE, CORNER


@dataclass
class Piece:
    position: Tuple[int, int, int]
    colors: Tuple

    def __str__(self):
        colors = "".join(c for c in self.colors if c is not None)
        return f"({self.type}, {colors}, {self.position})"

    def __post_init__(self):
        assert all(p in (-1, 0, 1) for p in self.position)
        assert len(self.colors) == 3
        self.colors = list(self.colors)
        self._set_piece_type()

    def _set_piece_type(self):
        if self.colors.count(None) == 2:
            self.type = FACE
        elif self.colors.count(None) == 1:
            self.type = EDGE
        elif self.colors.count(None) == 0:
            self.type = CORNER
        else:
            raise ValueError(f"Must have 1, 2, or 3 colors, given: {self.colors}")
