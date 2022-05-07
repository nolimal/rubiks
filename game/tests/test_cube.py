import pytest

from constants import BACK
from constants import DOWN
from constants import FRONT
from constants import LEFT
from constants import RIGHT
from constants import UP
from game.cube import Cube
from game.matrix import Matrix
from game.piece import Piece
from game.point import Point


def test_class_cube_works_with_cube_str(cube):
    assert isinstance(cube, Cube)


def test_class_cube_works_also_with_cube_instance(cube):
    assert isinstance(Cube(cube), Cube)


def test_cube_is_not_solved(cube):
    assert not cube.is_solved()


def test_cube_is_solved(solved_cube):
    assert solved_cube.is_solved()


def test_str_(cube):
    assert isinstance(cube.__str__(), str)


def test_flat_str(cube):
    assert isinstance(cube.flat_str(), str)


@pytest.fixture
def rotation_matrix():
    return Matrix([0, 1, 0, -1, 0, 0, 0, 0, 1])


@pytest.mark.parametrize("given_axis", [FRONT, BACK, UP, DOWN, LEFT, RIGHT])
def test__face(given_axis):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    pieces = cube._face(given_axis)
    count_faces = 0
    count_edges = 0
    count_corners = 0
    for p in pieces:
        if p.type == "face":
            count_faces += 1
        elif p.type == "edge":
            count_edges += 1
        else:
            count_corners += 1
    assert count_faces == 1
    assert count_edges == 4
    assert count_corners == 4


@pytest.mark.parametrize(
    "given_plane, contained_piece",
    [
        (FRONT + UP, Piece(position=Point(0, 1, 0), colors=(None, "U", None))),
        (
                FRONT + RIGHT,
                Piece(position=Point(1, 0, 0), colors=("R", None, None)),
        ),
        (UP + RIGHT, Piece(position=Point(1, 0, 0), colors=("R", None, None))),
    ],
)
def test__slice(given_plane, contained_piece):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    pieces = cube._slice(given_plane)
    assert len(pieces) == 8
    assert contained_piece in pieces


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "U")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "D")),
                        Piece(position=Point(-1, -1, 0), colors=("L", "F", None)),
                        Piece(position=Point(-1, 1, 0), colors=("L", "B", None)),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "F", "U")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "B", "U")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "F", "D")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "B", "D")),
                ),
        )
    ],
)
def test_L_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.L()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "U")),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "D")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "F", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "B", None)),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "F", "U")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "B", "U")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "F", "D")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "B", "D")),
                ),
        )
    ],
)
def test_Li_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Li()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 0, -1), colors=("R", None, "U")),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "D")),
                        Piece(position=Point(1, 1, 0), colors=("R", "F", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "B", None)),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, -1), colors=("R", "F", "U")),
                        Piece(position=Point(1, -1, -1), colors=("R", "B", "U")),
                        Piece(position=Point(1, 1, 1), colors=("R", "F", "D")),
                        Piece(position=Point(1, -1, 1), colors=("R", "B", "D")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_R_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.R()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 0, 1), colors=("R", None, "U")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "D")),
                        Piece(position=Point(1, -1, 0), colors=("R", "F", None)),
                        Piece(position=Point(1, 1, 0), colors=("R", "B", None)),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, -1, 1), colors=("R", "F", "U")),
                        Piece(position=Point(1, 1, 1), colors=("R", "B", "U")),
                        Piece(position=Point(1, -1, -1), colors=("R", "F", "D")),
                        Piece(position=Point(1, 1, -1), colors=("R", "B", "D")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_Ri_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Ri()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "R")),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "L")),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(-1, 1, 0), colors=("F", "U", None)),
                        Piece(position=Point(1, 1, 0), colors=("B", "U", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(-1, 1, 1), colors=("F", "U", "R")),
                        Piece(position=Point(1, 1, 1), colors=("B", "U", "R")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, -1), colors=("F", "U", "L")),
                        Piece(position=Point(1, 1, -1), colors=("B", "U", "L")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_U_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.U()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "R")),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "L")),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(1, 1, 0), colors=("F", "U", None)),
                        Piece(position=Point(-1, 1, 0), colors=("B", "U", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, -1), colors=("F", "U", "R")),
                        Piece(position=Point(-1, 1, -1), colors=("B", "U", "R")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(1, 1, 1), colors=("F", "U", "L")),
                        Piece(position=Point(-1, 1, 1), colors=("B", "U", "L")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_Ui_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Ui()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "R")),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "L")),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(1, -1, 0), colors=("F", "D", None)),
                        Piece(position=Point(-1, -1, 0), colors=("B", "D", None)),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, -1), colors=("F", "D", "R")),
                        Piece(position=Point(-1, -1, -1), colors=("B", "D", "R")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("F", "D", "L")),
                        Piece(position=Point(-1, -1, 1), colors=("B", "D", "L")),
                ),
        )
    ],
)
def test_D_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.D()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "R")),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "L")),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(-1, -1, 0), colors=("F", "D", None)),
                        Piece(position=Point(1, -1, 0), colors=("B", "D", None)),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("F", "D", "R")),
                        Piece(position=Point(1, -1, 1), colors=("B", "D", "R")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, -1), colors=("F", "D", "L")),
                        Piece(position=Point(1, -1, -1), colors=("B", "D", "L")),
                ),
        )
    ],
)
def test_Di_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Di()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "R", "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(0, 1, 1), colors=(None, "L", "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(1, 0, 1), colors=("U", None, "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(-1, 0, 1), colors=("D", None, "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, -1, 1), colors=("U", "R", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("D", "R", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(1, 1, 1), colors=("U", "L", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("D", "L", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_F_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.F()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(0, 1, 1), colors=(None, "R", "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "L", "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(-1, 0, 1), colors=("U", None, "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(1, 0, 1), colors=("D", None, "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(-1, 1, 1), colors=("U", "R", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, 1, 1), colors=("D", "R", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("U", "L", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("D", "L", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_Fi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Fi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "R", "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "L", "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(-1, 0, -1), colors=("U", None, "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(1, 0, -1), colors=("D", None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("U", "R", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, 1, -1), colors=("D", "R", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("U", "L", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("D", "L", "B")),
                ),
        )
    ],
)
def test_B_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.B()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "R", "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "L", "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(1, 0, -1), colors=("U", None, "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(-1, 0, -1), colors=("D", None, "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, -1, -1), colors=("U", "R", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("D", "R", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("U", "L", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("D", "L", "B")),
                ),
        )
    ],
)
def test_Bi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Bi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "U")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "D")),
                        Piece(position=Point(0, -1, 0), colors=(None, "F", None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "B", None)),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "F", "U")),
                        Piece(position=Point(0, 1, 1), colors=(None, "B", "U")),
                        Piece(position=Point(0, -1, -1), colors=(None, "F", "D")),
                        Piece(position=Point(0, 1, -1), colors=(None, "B", "D")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_M_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.M()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "U")),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "D")),
                        Piece(position=Point(0, 1, 0), colors=(None, "F", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "B", None)),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, 1, -1), colors=(None, "F", "U")),
                        Piece(position=Point(0, -1, -1), colors=(None, "B", "U")),
                        Piece(position=Point(0, 1, 1), colors=(None, "F", "D")),
                        Piece(position=Point(0, -1, 1), colors=(None, "B", "D")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_Mi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.Mi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, 0, -1), colors=(None, None, "R")),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "L")),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(1, 0, 0), colors=("F", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("B", None, None)),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(1, 0, -1), colors=("F", None, "R")),
                        Piece(position=Point(-1, 0, -1), colors=("B", None, "R")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(1, 0, 1), colors=("F", None, "L")),
                        Piece(position=Point(-1, 0, 1), colors=("B", None, "L")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_E_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.E()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, 0, 1), colors=(None, None, "R")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "L")),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(-1, 0, 0), colors=("F", None, None)),
                        Piece(position=Point(1, 0, 0), colors=("B", None, None)),
                ),
                (
                        Piece(position=Point(1, 1, 0), colors=("R", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "D", None)),
                        Piece(position=Point(-1, 0, 1), colors=("F", None, "R")),
                        Piece(position=Point(1, 0, 1), colors=("B", None, "R")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "D", None)),
                        Piece(position=Point(-1, 0, -1), colors=("F", None, "L")),
                        Piece(position=Point(1, 0, -1), colors=("B", None, "L")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_Ei_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.Ei()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, -1, 0), colors=(None, "R", None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "L", None)),
                        Piece(position=Point(1, 0, 0), colors=("U", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("D", None, None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, -1, 0), colors=("U", "R", None)),
                        Piece(position=Point(-1, -1, 0), colors=("D", "R", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(1, 1, 0), colors=("U", "L", None)),
                        Piece(position=Point(-1, 1, 0), colors=("D", "L", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_S_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.S()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, 1, 0), colors=(None, "R", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "L", None)),
                        Piece(position=Point(-1, 0, 0), colors=("U", None, None)),
                        Piece(position=Point(1, 0, 0), colors=("D", None, None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(-1, 1, 0), colors=("U", "R", None)),
                        Piece(position=Point(1, 1, 0), colors=("D", "R", None)),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "B")),
                        Piece(position=Point(-1, -1, 0), colors=("U", "L", None)),
                        Piece(position=Point(1, -1, 0), colors=("D", "L", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "B")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "B")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "B")),
                ),
                (
                        Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
                        Piece(position=Point(1, 1, -1), colors=("R", "U", "B")),
                        Piece(position=Point(1, -1, 1), colors=("R", "D", "F")),
                        Piece(position=Point(1, -1, -1), colors=("R", "D", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "U", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "D", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "D", "B")),
                ),
        )
    ],
)
def test_Si_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.Si()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "U")),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "D")),
                        Piece(position=Point(0, 1, 0), colors=(None, "F", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "B", None)),
                ),
                (
                        Piece(position=Point(1, 0, -1), colors=("R", None, "U")),
                        Piece(position=Point(1, 0, 1), colors=("R", None, "D")),
                        Piece(position=Point(1, 1, 0), colors=("R", "F", None)),
                        Piece(position=Point(1, -1, 0), colors=("R", "B", None)),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "U")),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "D")),
                        Piece(position=Point(-1, 1, 0), colors=("L", "F", None)),
                        Piece(position=Point(-1, -1, 0), colors=("L", "B", None)),
                        Piece(position=Point(0, 1, -1), colors=(None, "F", "U")),
                        Piece(position=Point(0, -1, -1), colors=(None, "B", "U")),
                        Piece(position=Point(0, 1, 1), colors=(None, "F", "D")),
                        Piece(position=Point(0, -1, 1), colors=(None, "B", "D")),
                ),
                (
                        Piece(position=Point(1, 1, -1), colors=("R", "F", "U")),
                        Piece(position=Point(1, -1, -1), colors=("R", "B", "U")),
                        Piece(position=Point(1, 1, 1), colors=("R", "F", "D")),
                        Piece(position=Point(1, -1, 1), colors=("R", "B", "D")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "F", "U")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "B", "U")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "F", "D")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "B", "D")),
                ),
        )
    ],
)
def test_X_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.X()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(1, 0, 0), colors=("R", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("L", None, None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "U")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "D")),
                        Piece(position=Point(0, -1, 0), colors=(None, "F", None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "B", None)),
                ),
                (
                        Piece(position=Point(1, 0, 1), colors=("R", None, "U")),
                        Piece(position=Point(1, 0, -1), colors=("R", None, "D")),
                        Piece(position=Point(1, -1, 0), colors=("R", "F", None)),
                        Piece(position=Point(1, 1, 0), colors=("R", "B", None)),
                        Piece(position=Point(-1, 0, 1), colors=("L", None, "U")),
                        Piece(position=Point(-1, 0, -1), colors=("L", None, "D")),
                        Piece(position=Point(-1, -1, 0), colors=("L", "F", None)),
                        Piece(position=Point(-1, 1, 0), colors=("L", "B", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "F", "U")),
                        Piece(position=Point(0, 1, 1), colors=(None, "B", "U")),
                        Piece(position=Point(0, -1, -1), colors=(None, "F", "D")),
                        Piece(position=Point(0, 1, -1), colors=(None, "B", "D")),
                ),
                (
                        Piece(position=Point(1, -1, 1), colors=("R", "F", "U")),
                        Piece(position=Point(1, 1, 1), colors=("R", "B", "U")),
                        Piece(position=Point(1, -1, -1), colors=("R", "F", "D")),
                        Piece(position=Point(1, 1, -1), colors=("R", "B", "D")),
                        Piece(position=Point(-1, -1, 1), colors=("L", "F", "U")),
                        Piece(position=Point(-1, 1, 1), colors=("L", "B", "U")),
                        Piece(position=Point(-1, -1, -1), colors=("L", "F", "D")),
                        Piece(position=Point(-1, 1, -1), colors=("L", "B", "D")),
                ),
        )
    ],
)
def test_Xi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Xi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, 0, 1), colors=(None, None, "R")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "L")),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(-1, 0, 0), colors=("F", None, None)),
                        Piece(position=Point(1, 0, 0), colors=("B", None, None)),
                ),
                (
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "R")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "R")),
                        Piece(position=Point(-1, 0, 1), colors=("F", None, "R")),
                        Piece(position=Point(1, 0, 1), colors=("B", None, "R")),
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "L")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "L")),
                        Piece(position=Point(-1, 0, -1), colors=("F", None, "L")),
                        Piece(position=Point(1, 0, -1), colors=("B", None, "L")),
                        Piece(position=Point(-1, 1, 0), colors=("F", "U", None)),
                        Piece(position=Point(1, 1, 0), colors=("B", "U", None)),
                        Piece(position=Point(-1, -1, 0), colors=("F", "D", None)),
                        Piece(position=Point(1, -1, 0), colors=("B", "D", None)),
                ),
                (
                        Piece(position=Point(-1, 1, 1), colors=("F", "U", "R")),
                        Piece(position=Point(1, 1, 1), colors=("B", "U", "R")),
                        Piece(position=Point(-1, -1, 1), colors=("F", "D", "R")),
                        Piece(position=Point(1, -1, 1), colors=("B", "D", "R")),
                        Piece(position=Point(-1, 1, -1), colors=("F", "U", "L")),
                        Piece(position=Point(1, 1, -1), colors=("B", "U", "L")),
                        Piece(position=Point(-1, -1, -1), colors=("F", "D", "L")),
                        Piece(position=Point(1, -1, -1), colors=("B", "D", "L")),
                ),
        )
    ],
)
def test_Y_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Y()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, 0, -1), colors=(None, None, "R")),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "L")),
                        Piece(position=Point(0, 1, 0), colors=(None, "U", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "D", None)),
                        Piece(position=Point(1, 0, 0), colors=("F", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("B", None, None)),
                ),
                (
                        Piece(position=Point(0, 1, -1), colors=(None, "U", "R")),
                        Piece(position=Point(0, -1, -1), colors=(None, "D", "R")),
                        Piece(position=Point(1, 0, -1), colors=("F", None, "R")),
                        Piece(position=Point(-1, 0, -1), colors=("B", None, "R")),
                        Piece(position=Point(0, 1, 1), colors=(None, "U", "L")),
                        Piece(position=Point(0, -1, 1), colors=(None, "D", "L")),
                        Piece(position=Point(1, 0, 1), colors=("F", None, "L")),
                        Piece(position=Point(-1, 0, 1), colors=("B", None, "L")),
                        Piece(position=Point(1, 1, 0), colors=("F", "U", None)),
                        Piece(position=Point(-1, 1, 0), colors=("B", "U", None)),
                        Piece(position=Point(1, -1, 0), colors=("F", "D", None)),
                        Piece(position=Point(-1, -1, 0), colors=("B", "D", None)),
                ),
                (
                        Piece(position=Point(1, 1, -1), colors=("F", "U", "R")),
                        Piece(position=Point(-1, 1, -1), colors=("B", "U", "R")),
                        Piece(position=Point(1, -1, -1), colors=("F", "D", "R")),
                        Piece(position=Point(-1, -1, -1), colors=("B", "D", "R")),
                        Piece(position=Point(1, 1, 1), colors=("F", "U", "L")),
                        Piece(position=Point(-1, 1, 1), colors=("B", "U", "L")),
                        Piece(position=Point(1, -1, 1), colors=("F", "D", "L")),
                        Piece(position=Point(-1, -1, 1), colors=("B", "D", "L")),
                ),
        )
    ],
)
def test_Yi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Yi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, -1, 0), colors=(None, "R", None)),
                        Piece(position=Point(0, 1, 0), colors=(None, "L", None)),
                        Piece(position=Point(1, 0, 0), colors=("U", None, None)),
                        Piece(position=Point(-1, 0, 0), colors=("D", None, None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(1, -1, 0), colors=("U", "R", None)),
                        Piece(position=Point(-1, -1, 0), colors=("D", "R", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "R", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "R", "B")),
                        Piece(position=Point(1, 1, 0), colors=("U", "L", None)),
                        Piece(position=Point(-1, 1, 0), colors=("D", "L", None)),
                        Piece(position=Point(0, 1, 1), colors=(None, "L", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "L", "B")),
                        Piece(position=Point(1, 0, 1), colors=("U", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("U", None, "B")),
                        Piece(position=Point(-1, 0, 1), colors=("D", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("D", None, "B")),
                ),
                (
                        Piece(position=Point(1, -1, 1), colors=("U", "R", "F")),
                        Piece(position=Point(1, -1, -1), colors=("U", "R", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("D", "R", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("D", "R", "B")),
                        Piece(position=Point(1, 1, 1), colors=("U", "L", "F")),
                        Piece(position=Point(1, 1, -1), colors=("U", "L", "B")),
                        Piece(position=Point(-1, 1, 1), colors=("D", "L", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("D", "L", "B")),
                ),
        )
    ],
)
def test_Z_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Z()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [
        (
                (
                        Piece(position=Point(0, 1, 0), colors=(None, "R", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "L", None)),
                        Piece(position=Point(-1, 0, 0), colors=("U", None, None)),
                        Piece(position=Point(1, 0, 0), colors=("D", None, None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(-1, 1, 0), colors=("U", "R", None)),
                        Piece(position=Point(1, 1, 0), colors=("D", "R", None)),
                        Piece(position=Point(0, 1, 1), colors=(None, "R", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "R", "B")),
                        Piece(position=Point(-1, -1, 0), colors=("U", "L", None)),
                        Piece(position=Point(1, -1, 0), colors=("D", "L", None)),
                        Piece(position=Point(0, -1, 1), colors=(None, "L", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "L", "B")),
                        Piece(position=Point(-1, 0, 1), colors=("U", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("U", None, "B")),
                        Piece(position=Point(1, 0, 1), colors=("D", None, "F")),
                        Piece(position=Point(1, 0, -1), colors=("D", None, "B")),
                ),
                (
                        Piece(position=Point(-1, 1, 1), colors=("U", "R", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("U", "R", "B")),
                        Piece(position=Point(1, 1, 1), colors=("D", "R", "F")),
                        Piece(position=Point(1, 1, -1), colors=("D", "R", "B")),
                        Piece(position=Point(-1, -1, 1), colors=("U", "L", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("U", "L", "B")),
                        Piece(position=Point(1, -1, 1), colors=("D", "L", "F")),
                        Piece(position=Point(1, -1, -1), colors=("D", "L", "B")),
                ),
        )
    ],
)
def test_Zi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Zi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "move_str, expected_faces, expected_edges, expected_corners",
    [
        (
                "Zi R",
                (
                        Piece(position=Point(0, 1, 0), colors=(None, "R", None)),
                        Piece(position=Point(0, -1, 0), colors=(None, "L", None)),
                        Piece(position=Point(-1, 0, 0), colors=("U", None, None)),
                        Piece(position=Point(1, 0, 0), colors=("D", None, None)),
                        Piece(position=Point(0, 0, 1), colors=(None, None, "F")),
                        Piece(position=Point(0, 0, -1), colors=(None, None, "B")),
                ),
                (
                        Piece(position=Point(-1, 1, 0), colors=("U", "R", None)),
                        Piece(position=Point(1, 0, -1), colors=("D", None, "R")),
                        Piece(position=Point(0, 1, 1), colors=(None, "R", "F")),
                        Piece(position=Point(0, 1, -1), colors=(None, "R", "B")),
                        Piece(position=Point(-1, -1, 0), colors=("U", "L", None)),
                        Piece(position=Point(1, 0, 1), colors=("D", None, "L")),
                        Piece(position=Point(0, -1, 1), colors=(None, "L", "F")),
                        Piece(position=Point(0, -1, -1), colors=(None, "L", "B")),
                        Piece(position=Point(-1, 0, 1), colors=("U", None, "F")),
                        Piece(position=Point(-1, 0, -1), colors=("U", None, "B")),
                        Piece(position=Point(1, 1, 0), colors=("D", "F", None)),
                        Piece(position=Point(1, -1, 0), colors=("D", "B", None)),
                ),
                (
                        Piece(position=Point(-1, 1, 1), colors=("U", "R", "F")),
                        Piece(position=Point(-1, 1, -1), colors=("U", "R", "B")),
                        Piece(position=Point(1, 1, -1), colors=("D", "F", "R")),
                        Piece(position=Point(1, -1, -1), colors=("D", "B", "R")),
                        Piece(position=Point(-1, -1, 1), colors=("U", "L", "F")),
                        Piece(position=Point(-1, -1, -1), colors=("U", "L", "B")),
                        Piece(position=Point(1, 1, 1), colors=("D", "F", "L")),
                        Piece(position=Point(1, -1, 1), colors=("D", "B", "L")),
                ),
        )
    ],
)
def test_move_sequence_identical_to_separate_moves(
        move_str, expected_faces, expected_edges, expected_corners
):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    cube_alternative = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    assert not cube_alternative.faces == expected_faces
    assert not cube_alternative.edges == expected_edges
    assert not cube_alternative.corners == expected_corners
    cube.sequence(move_str)
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube_alternative.Zi()
    cube_alternative.R()
    assert cube_alternative.faces == expected_faces
    assert cube_alternative.edges == expected_edges
    assert cube_alternative.corners == expected_corners


@pytest.mark.parametrize(
    "colors, expected_piece",
    [
        (
                ["R", "U", "F"],
                Piece(position=Point(1, 1, 1), colors=("R", "U", "F")),
        ),
        (
                ["L", "U", "B"],
                Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
        ),
        ([None, "U", "F"], None),
    ],
)
def test_find_piece(colors, expected_piece):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    piece = cube.find_piece(*colors)
    assert piece == expected_piece


@pytest.mark.parametrize(
    "x, y, z, expected_piece",
    [
        (1, 1, 1, Piece(position=Point(1, 1, 1), colors=("R", "U", "F"))),
        (
                (-1),
                1,
                (-1),
                Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
        ),
        (0, 1, 1, Piece(position=Point(0, 1, 1), colors=(None, "U", "F"))),
    ],
)
def test_get_piece(x, y, z, expected_piece):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    piece = cube.get_piece(x, y, z)
    assert piece == expected_piece


@pytest.mark.parametrize(
    "arguments, expected_piece",
    [
        ([1, 1, 1], Piece(position=Point(1, 1, 1), colors=("R", "U", "F"))),
        (
                [(-1), 1, (-1)],
                Piece(position=Point(-1, 1, -1), colors=("L", "U", "B")),
        ),
        ([0, 1, 1], Piece(position=Point(0, 1, 1), colors=(None, "U", "F"))),
    ],
)
def test__getitem__(arguments, expected_piece):
    cube = Cube(
        "UUU"
        "UUU"
        "UUU"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "LLLFFFRRRBBB"
        "DDD"
        "DDD"
        "DDD"
    )
    piece = cube.__getitem__(*arguments)
    assert piece == expected_piece


@pytest.mark.parametrize(
    "cube1, cube2, expected",
    [
        ("cube", "cube", True),
        ("solved_cube", "solved_cube", True),
        ("solved_cube", "cube", False),
    ],
)
def test__eq__(cube1, cube2, expected, request):
    cube1 = request.getfixturevalue(cube1)
    cube2 = request.getfixturevalue(cube2)
    assert expected == cube1.__eq__(cube2)


@pytest.mark.parametrize(
    "cube1, cube2, expected",
    [
        ("cube", "cube", False),
        ("solved_cube", "solved_cube", False),
        ("solved_cube", "cube", True),
    ],
)
def test__ne__(cube1, cube2, expected, request):
    cube1 = request.getfixturevalue(cube1)
    cube2 = request.getfixturevalue(cube2)
    assert expected == cube1.__ne__(cube2)


@pytest.mark.parametrize(
    "cube1, expected_color", [("cube", "B"), ("solved_cube", "L")]
)
def test_left_color(cube1, expected_color, request):
    cube1 = request.getfixturevalue(cube1)
    assert expected_color == cube1.left_color()


@pytest.mark.parametrize(
    "cube1, expected_color", [("cube", "F"), ("solved_cube", "R")]
)
def test_right_color(cube1, expected_color, request):
    cube1 = request.getfixturevalue(cube1)
    assert expected_color == cube1.right_color()


@pytest.mark.parametrize(
    "cube1, expected_color", [("cube", "R"), ("solved_cube", "U")]
)
def test_up_color(cube1, expected_color, request):
    cube1 = request.getfixturevalue(cube1)
    assert expected_color == cube1.up_color()


@pytest.mark.parametrize(
    "cube1, expected_color", [("cube", "L"), ("solved_cube", "D")]
)
def test_down_color(cube1, expected_color, request):
    cube1 = request.getfixturevalue(cube1)
    assert expected_color == cube1.down_color()


@pytest.mark.parametrize(
    "cube1, expected_color", [("cube", "U"), ("solved_cube", "F")]
)
def test_front_color(cube1, expected_color, request):
    cube1 = request.getfixturevalue(cube1)
    assert expected_color == cube1.front_color()


@pytest.mark.parametrize(
    "cube1, expected_color", [("cube", "D"), ("solved_cube", "B")]
)
def test_back_color(cube1, expected_color, request):
    cube1 = request.getfixturevalue(cube1)
    assert expected_color == cube1.back_color()


@pytest.mark.parametrize(
    "cube1, expected_color",
    [
        (
                "cube",
                [
                    "D",
                    "L",
                    "U",
                    "R",
                    "R",
                    "D",
                    "F",
                    "F",
                    "U",
                    "B",
                    "B",
                    "L",
                    "D",
                    "D",
                    "R",
                    "B",
                    "R",
                    "B",
                    "L",
                    "D",
                    "L",
                    "R",
                    "B",
                    "F",
                    "R",
                    "U",
                    "U",
                    "L",
                    "F",
                    "B",
                    "D",
                    "D",
                    "U",
                    "F",
                    "B",
                    "R",
                    "B",
                    "B",
                    "R",
                    "F",
                    "U",
                    "D",
                    "F",
                    "L",
                    "U",
                    "D",
                    "L",
                    "U",
                    "U",
                    "L",
                    "F",
                    "L",
                    "F",
                    "R",
                ],
        ),
        (
                "solved_cube",
                [
                    "U",
                    "U",
                    "U",
                    "U",
                    "U",
                    "U",
                    "U",
                    "U",
                    "U",
                    "L",
                    "L",
                    "L",
                    "F",
                    "F",
                    "F",
                    "R",
                    "R",
                    "R",
                    "B",
                    "B",
                    "B",
                    "L",
                    "L",
                    "L",
                    "F",
                    "F",
                    "F",
                    "R",
                    "R",
                    "R",
                    "B",
                    "B",
                    "B",
                    "L",
                    "L",
                    "L",
                    "F",
                    "F",
                    "F",
                    "R",
                    "R",
                    "R",
                    "B",
                    "B",
                    "B",
                    "D",
                    "D",
                    "D",
                    "D",
                    "D",
                    "D",
                    "D",
                    "D",
                    "D",
                ],
        ),
    ],
)
def test__color_list(cube1, expected_color, request):
    cube1 = request.getfixturevalue(cube1)
    colors = cube1._color_list()
    assert expected_color == colors
