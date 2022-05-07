from dataclasses import dataclass
from constants import FACE, EDGE, CORNER
from game.point import Point
from typing import Union, Tuple


@dataclass
class Piece:
    position: Union[Point, Tuple[int, int, int]]
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
            raise ValueError(
                f"Must have 1, 2, or 3 colors, given: {self.colors}"
            )

    def rotate(self, matrix):
        """Rotation matrix multiplication for a single piece"""
        before = self.position
        self.position = matrix * self.position

        # we need to swap the positions of two things in self.colors
        # so colors appear on the correct faces.
        # rot gives us the axes to swap between.
        rot = self.position - before
        if not any(rot):
            return  # no change occurred
        if rot.count(0) == 2:
            rot += matrix * rot

        assert rot.count(0) == 1, (
            f"There is a bug in the Piece.rotate() method!"
            f"\nbefore: {before}"
            f"\nafter: {self.position}"
            f"\nchanges: {rot}"
        )

        i, j = (i for i, x in enumerate(rot) if x != 0)
        self.colors[i], self.colors[j] = self.colors[j], self.colors[i]
