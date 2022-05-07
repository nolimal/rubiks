import pytest

from game.cube import Cube


@pytest.fixture
def cube_str():
    return (
        "DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR"
    )


@pytest.fixture
def cube(cube_str):
    return Cube(cube_str)


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
