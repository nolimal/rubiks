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
                Piece(position=Point(-1, 0, 0), colors=['B', None, None]),
        ),
        (
                "cube",
                "right_piece",
                Piece(position=Point(1, 0, 0), colors=['F', None, None]),
        ),
        (
                "cube",
                "up_piece",
                Piece(position=Point(0, 1, 0), colors=[None, 'R', None]),
        ),
        (
                "cube",
                "down_piece",
                Piece(position=Point(0, -1, 0), colors=[None, 'L', None]),
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


def test_cross(solver):
    solver.cross()
    assert solver
