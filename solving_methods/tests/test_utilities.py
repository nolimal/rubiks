import pytest
from constants import BACK
from constants import DOWN
from constants import FRONT
from constants import LEFT
from constants import RIGHT
from constants import UP
from game.point import Point
from solving_methods.utilities import get_rotations_from_face


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


def test_get_rotations_from_face_non_face(non_face):
    assert get_rotations_from_face(non_face) is None
