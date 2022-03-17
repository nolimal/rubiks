import pytest
from game.piece import Piece
from constants import FACE


def test_nothing():
    assert True


@pytest.fixture
def position_face_r():
    return (1, 0, 0)


@pytest.fixture
def color_face_r_red():
    return ("Red", None, None)


@pytest.fixture
def piece(position_face_r, color_face_r_red):
    return Piece(position_face_r, color_face_r_red)


def test_class_piece_exists(piece):
    assert isinstance(piece, Piece)


def test_set_piece_type(piece):
    assert piece.type == FACE


def test_str_(piece):
    assert piece.__str__().__contains__(FACE)
    assert piece.__str__().__contains__("Red")
