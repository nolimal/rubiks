from game.point import Point
from typing import Union, List
from dataclasses import dataclass


@dataclass
class Matrix:
    """A 3x3 matrix"""

    vals: Union[List[int], List[List[int]]]

    def __post_init__(self):
        if len(self.vals) == 9:
            self.vals = list(self.vals)
        elif len(self.vals) == 3:
            try:
                self.vals = [x for y in self.vals for x in y]
            except:
                self.vals = []
        if len(self.vals) != 9:
            raise ValueError(f"Matrix requires 9 items, got {self.vals}")

    def __str__(self):
        return "[{}, {}, {},\n" " {}, {}, {},\n" " {}, {}, {}]".format(*self.vals)

    def __repr__(self):
        return (
            "Matrix({}, {}, {},\n"
            "       {}, {}, {},\n"
            "       {}, {}, {})".format(*self.vals)
        )

    def __eq__(self, other):
        return self.vals == other.vals

    def __add__(self, other):
        return Matrix(a + b for a, b in zip(self.vals, other.vals))

    def __sub__(self, other):
        return Matrix(a - b for a, b in zip(self.vals, other.vals))

    def __iadd__(self, other):
        self.vals = [a + b for a, b in zip(self.vals, other.vals)]
        return self

    def __isub__(self, other):
        self.vals = [a - b for a, b in zip(self.vals, other.vals)]
        return self

    def __mul__(self, other):
        """Do Matrix-Matrix or Matrix-Point multiplication."""
        if isinstance(other, Point):
            return Point(tuple([other.dot(Point(tuple(row))) for row in self.rows()]))
        elif isinstance(other, Matrix):
            return Matrix(
                Point(row).dot(Point(col))
                for row in self.rows()
                for col in other.cols()
            )

    def rows(self):
        yield self.vals[0:3]
        yield self.vals[3:6]
        yield self.vals[6:9]

    def cols(self):
        yield self.vals[0:9:3]
        yield self.vals[1:9:3]
        yield self.vals[2:9:3]
