from __future__ import annotations
from typing import Tuple, Union, Optional
from dataclasses import dataclass


@dataclass
class Point:
    """A 3D point/vector"""
    x: Union[Tuple, int]
    y: Optional[int] = None
    z: Optional[int] = None

    def __post_init__(self):
        if isinstance(self.x, (tuple, Point)):
            t = self.x
            self.x = t[0]
            self.y = t[1]
            self.z = t[2]
        if any(component is None for component in self):
            raise ValueError(f"Point contains 'None': {self}")

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        return "Point" + str(self)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, value):
        return Point(self.x * value, self.y * value, self.z * value)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Point(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def count(self, val):
        return int(self.x == val) + int(self.y == val) + int(self.z == val)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        raise IndexError("Point index out of range")

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __eq__(self, other):
        if isinstance(other, (tuple, list)):
            return self.x == other[0] and self.y == other[1] and self.z == other[2]
        return (isinstance(other, self.__class__) and self.x == other.x
                and self.y == other.y and self.z == other.z)

    def __ne__(self, other):
        return not (self == other)
