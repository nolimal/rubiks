import pytest

from game.piece import Piece
from game.point import Point
from solving_methods.solver import Solver


def test_solver_class_exists(cube):
    solver = Solver(cube)
    assert isinstance(solver, Solver)


def test_solver_initiation(cube):
    solver = Solver(cube)
    assert cube.__eq__(solver.cube)
    assert solver.colors - {" ", "U", "R", "F", "L", "D", "B"} == set()
    assert solver.moves == []


@pytest.mark.parametrize(
    "cube1, piece, expected_piece",
    [
        (
                "cube",
                "left_piece",
                Piece(position=Point(-1, 0, 0), colors=("B", None, None)),
        ),
        (
                "cube",
                "right_piece",
                Piece(position=Point(1, 0, 0), colors=("F", None, None)),
        ),
        (
                "cube",
                "up_piece",
                Piece(position=Point(0, 1, 0), colors=(None, "R", None)),
        ),
        (
                "cube",
                "down_piece",
                Piece(position=Point(0, -1, 0), colors=(None, "L", None)),
        ),
    ],
)
def test_solver_pieces(cube1, piece, expected_piece, request):
    cube = request.getfixturevalue(cube1)
    solver = Solver(cube)
    assert solver.__getattribute__(piece) == expected_piece


@pytest.fixture
def solver(cube):
    return Solver(cube)


def test_solve_is_callable(solver):
    assert callable(solver.solve)


@pytest.fixture
def _after_cross():
    return "DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR"


def test_cross(solver, _after_cross):
    solver.cross()
    assert solver.cube.cube_str == _after_cross
    print(solver.cube)


@pytest.fixture
def _after_cross_corners():
    return "DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR"


def test_cross_corners(solver, _after_cross_corners):
    solver.cross()
    solver.cross_corners()
    assert solver.cube.cube_str == _after_cross_corners
    print(solver.cube)


@pytest.fixture
def _after_second_layer():
    return "DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR"


def test_second_layer(solver, _after_second_layer):
    solver.cross()
    solver.cross_corners()
    solver.second_layer()
    assert solver.cube.cube_str == _after_second_layer
    print(solver.cube)


@pytest.fixture
def _after_back_face_edges():
    return "DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR"


def test_back_face_edges(solver, _after_back_face_edges):
    solver.cross()
    solver.cross_corners()
    solver.second_layer()
    solver.back_face_edges()
    assert solver.cube.cube_str == _after_back_face_edges
    print(solver.cube)


@pytest.fixture
def _after_last_layer_corners_position():
    return "DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR"


def test_last_layer_corners_positions(
        solver, _after_last_layer_corners_position
):
    solver.cross()
    solver.cross_corners()
    solver.second_layer()
    solver.back_face_edges()
    solver.last_layer_corners_position()
    assert solver.cube.cube_str == _after_last_layer_corners_position
    print(solver.cube)
