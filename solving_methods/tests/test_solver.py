import pytest

from game.cube import Cube
from game.piece import Piece
from game.point import Point
from solving_methods.solver import Solver


@pytest.fixture
def solvable_cube_str():
    return (
        "DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR"
    )


@pytest.fixture
def solvable_cube(solvable_cube_str):
    return Cube(solvable_cube_str)


@pytest.fixture
def solved_cube_str():
    return (
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


@pytest.fixture
def solved_cube(solved_cube_str):
    return Cube(solved_cube_str)


def test_solver_class_exists(solvable_cube):
    solver = Solver(solvable_cube)
    assert isinstance(solver, Solver)


def test_solver_initiation(solvable_cube):
    solver = Solver(solvable_cube)
    assert solvable_cube.__eq__(solver.cube)
    assert solver.colors - {" ", "U", "R", "F", "L", "D", "B"} == set()
    assert solver.moves == []


@pytest.mark.parametrize(
    "cube1, piece, expected_piece",
    [
        (
                "solvable_cube",
                "left_piece",
                Piece(position=Point(-1, 0, 0), colors=['B', None, None]),
        ),
        (
                "solvable_cube",
                "right_piece",
                Piece(position=Point(1, 0, 0), colors=['F', None, None]),
        ),
        (
                "solvable_cube",
                "up_piece",
                Piece(position=Point(0, 1, 0), colors=[None, 'R', None]),
        ),
        (
                "solvable_cube",
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
def solver(solvable_cube):
    return Solver(solvable_cube)


def test_solve_is_callable(solver):
    assert callable(solver.solve)


def test_cross(solver):
    solver.cross()
    assert solver
