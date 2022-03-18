import pytest
from game.point import Point


def test_class_point_exists():
    assert callable(Point)


@pytest.fixture
def point():
    return Point(1, 0, 0)


def test_point_arguments(point):
    assert point.x == 1
    assert point.y == 0
    assert point.z == 0


@pytest.fixture
def point_tuple():
    return Point((0, 1, 0))


def test_point_tuple_arguments(point_tuple):
    assert point_tuple.x == 0
    assert point_tuple.y == 1
    assert point_tuple.z == 0


def test__str__(point):
    assert point.__str__() == "(1, 0, 0)"


def test__repr__(point):
    assert point.__repr__() == "Point(1, 0, 0)"


@pytest.fixture
def point_other():
    return Point(0, 1, 0)


def test__add__(point, point_other):
    assert point.__add__(point_other) == Point(1, 1, 0)


def test__sub__(point, point_other):
    assert point.__sub__(point_other) == Point(1, -1, 0)


def test_dot(point, point_other):
    assert point.dot(point_other) == 0


def test_cross(point, point_other):
    assert point.cross(point_other) == Point(0, 0, 1)
