import pytest
from solving_methods.utilities import get_rotations_from_face
from constants import RIGHT, LEFT, UP, DOWN, FRONT, BACK
from game.point import Point


@pytest.mark.parametrize(
    "face, expected_rotation_cw, expected_rotation_cc",
    [
        (RIGHT, "R", "Ri"),
        (LEFT, "L", "Li"),
        (UP, "U", "Ui"),
        (DOWN, "D", "Di"),
        (FRONT, "F", "Fi"),
        (BACK, "B", "Bi"),
    ],
)
def test_get_rotations_from_face(
        face, expected_rotation_cw, expected_rotation_cc
):
    rotation_cw, rotation_cc = get_rotations_from_face(face)
    assert expected_rotation_cw == rotation_cw
    assert expected_rotation_cc == rotation_cc


@pytest.fixture
def non_face():
    return Point(1, 1, 1)


def test_get_rotations_from_face(non_face):
    assert get_rotations_from_face(non_face) is None
