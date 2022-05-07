import pytest
from game.piece import Piece
from constants import FACE
from game.matrix import Matrix
from game.point import Point


def test_nothing():
    assert True


@pytest.fixture
def position_face_r():
    return Point(1, 0, 0)


@pytest.fixture
def color_face_r_red():
    return ("Red", None, None)


@pytest.fixture
def piece(position_face_r, color_face_r_red):
    return Piece(position_face_r, color_face_r_red)


def test_class_piece_exists(piece):
    assert isinstance(piece, Piece)


def test_str_(piece):
    assert piece.__str__().__contains__(FACE)
    assert piece.__str__().__contains__("Red")


def test_set_piece_type(piece):
    assert piece.type == FACE


@pytest.fixture
def rotation_matrix():
    return Matrix([0, 1, 0, -1, 0, 0, 0, 0, 1])


def test_rotate(piece, rotation_matrix):
    position_before = piece.position
    piece.rotate(rotation_matrix)
    assert piece.colors == [None, "Red", None]
    assert position_before != piece.position
    assert piece.position == Point(0, -1, 0)
