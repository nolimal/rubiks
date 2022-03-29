import pytest
from game.matrix import Matrix


@pytest.fixture
def input_list():
    return [1, 2, 3, 4, 5, 6, 7, 8, 1]


@pytest.fixture
def input_list_by_rows():
    return [[11, 12, 13], [14, 15, 16], [17, 18, 19]]


@pytest.fixture
def matrix(input_list):
    return Matrix(input_list)


def test_class_matrix_happy(matrix):
    assert isinstance(matrix, Matrix)


@pytest.fixture
def matrix_alternative(input_list_by_rows):
    return Matrix(input_list)


def test_class_matrix_alternative_happy(matrix):
    assert isinstance(matrix, Matrix)


@pytest.fixture
def corrupt_input():
    return [1, 2, 3, 4]


def test__post_init__raises(corrupt_input):
    with pytest.raises(ValueError):
        Matrix(corrupt_input)
