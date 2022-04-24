import pytest
from game.cube import Cube
from game.matrix import Matrix
from game.piece import Piece
from game.point import Point
from constants import FRONT, BACK, UP, DOWN, LEFT, RIGHT


@pytest.fixture
def cube_str():
    return ("DLU"
            "RRD"
            "FFU"
            "BBLDDRBRBLDL"
            "RBFRUULFB DDU"
            "FBRBBRFUDFLU"
            "DLU"
            "ULF"
            "LFR")


@pytest.fixture
def cube(cube_str):
    return Cube(cube_str)


def test_class_cube_works_with_cube_str(cube):
    assert isinstance(cube, Cube)


def test_class_cube_works_also_with_cube_instance(cube):
    assert isinstance(Cube(cube), Cube)


def test_cube_is_not_solved(cube):
    assert not cube.is_solved()


@pytest.fixture
def solved_cube_str():
    return ("UUU"
            "UUU"
            "UUU"
            "LLLFFFRRRBBB"
            "LLLFFFRRRBBB"
            "LLLFFFRRRBBB"
            "DDD"
            "DDD"
            "DDD")


@pytest.fixture
def solved_cube(solved_cube_str):
    return Cube(solved_cube_str)


def test_cube_is_solved(solved_cube):
    assert solved_cube.is_solved()


def test_str_(cube):
    assert isinstance(cube.__str__(), str)


@pytest.fixture
def rotation_matrix():
    return Matrix([0, 1, 0,
                   -1, 0, 0,
                   0, 0, 1])


@pytest.mark.parametrize(
    "given_axis",
    [FRONT,
     BACK,
     UP,
     DOWN,
     LEFT,
     RIGHT]
)
def test__face(given_axis):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
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
    [(FRONT + UP, Piece(position=Point(0, 1, 0), colors=[None, 'U', None])),
     (FRONT + RIGHT, Piece(position=Point(1, 0, 0), colors=['R', None, None])),
     (UP + RIGHT, Piece(position=Point(1, 0, 0), colors=['R', None, None]))]
)
def test__slice(given_plane, contained_piece):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    pieces = cube._slice(given_plane)
    assert len(pieces) == 8
    assert contained_piece in pieces


def test__rotate_face():
    pass


def test__rotate_pieces():
    pass


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B'])
       ),
      (
              Piece(position=Point(1, 1, 0), colors=['R', 'U', None]),
              Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
              Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
              Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
              Piece(position=Point(-1, 0, 1), colors=['L', None, 'U']),
              Piece(position=Point(-1, 0, -1), colors=['L', None, 'D']),
              Piece(position=Point(-1, -1, 0), colors=['L', 'F', None]),
              Piece(position=Point(-1, 1, 0), colors=['L', 'B', None]),
              Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
              Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
              Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
              Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B'])
      ),
      (
              Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']),
              Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
              Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
              Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
              Piece(position=Point(-1, -1, 1), colors=['L', 'F', 'U']),
              Piece(position=Point(-1, 1, 1), colors=['L', 'B', 'U']),
              Piece(position=Point(-1, -1, -1), colors=['L', 'F', 'D']),
              Piece(position=Point(-1, 1, -1), colors=['L', 'B', 'D']))
      )]
)
def test_L_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.L()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B'])),
      (
              Piece(position=Point(1, 1, 0), colors=['R', 'U', None]),
              Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
              Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
              Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
              Piece(position=Point(-1, 0, -1), colors=['L', None, 'U']),
              Piece(position=Point(-1, 0, 1), colors=['L', None, 'D']),
              Piece(position=Point(-1, 1, 0), colors=['L', 'F', None]),
              Piece(position=Point(-1, -1, 0), colors=['L', 'B', None]),
              Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
              Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
              Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
              Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'F', 'U']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'B', 'U']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'F', 'D']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'B', 'D']))
      )]
)
def test_Li_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Li()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
              Piece(position=Point(1, 0, -1), colors=['R', None, 'U']),
              Piece(position=Point(1, 0, 1), colors=['R', None, 'D']),
              Piece(position=Point(1, 1, 0), colors=['R', 'F', None]),
              Piece(position=Point(1, -1, 0), colors=['R', 'B', None]),
              Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
              Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
              Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
              Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
              Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
              Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
              Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
              Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (
              Piece(position=Point(1, 1, -1), colors=['R', 'F', 'U']),
              Piece(position=Point(1, -1, -1), colors=['R', 'B', 'U']),
              Piece(position=Point(1, 1, 1), colors=['R', 'F', 'D']),
              Piece(position=Point(1, -1, 1), colors=['R', 'B', 'D']),
              Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
              Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
              Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
              Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))
      )]
)
def test_R_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.R()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
              Piece(position=Point(1, 0, 1), colors=['R', None, 'U']),
              Piece(position=Point(1, 0, -1), colors=['R', None, 'D']),
              Piece(position=Point(1, -1, 0), colors=['R', 'F', None]),
              Piece(position=Point(1, 1, 0), colors=['R', 'B', None]),
              Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
              Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
              Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
              Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
              Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
              Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
              Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
              Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(1, -1, 1), colors=['R', 'F', 'U']), Piece(position=Point(1, 1, 1), colors=['R', 'B', 'U']),
       Piece(position=Point(1, -1, -1), colors=['R', 'F', 'D']),
       Piece(position=Point(1, 1, -1), colors=['R', 'B', 'D']), Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_Ri_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Ri()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
              Piece(position=Point(0, 1, 1), colors=[None, 'U', 'R']),
              Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
              Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
              Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
              Piece(position=Point(0, 1, -1), colors=[None, 'U', 'L']),
              Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
              Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
              Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
              Piece(position=Point(-1, 1, 0), colors=['F', 'U', None]),
              Piece(position=Point(1, 1, 0), colors=['B', 'U', None]),
              Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
              Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(-1, 1, 1), colors=['F', 'U', 'R']), Piece(position=Point(1, 1, 1), colors=['B', 'U', 'R']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, -1), colors=['F', 'U', 'L']),
       Piece(position=Point(1, 1, -1), colors=['B', 'U', 'L']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))
      )]
)
def test_U_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.U()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (Piece(position=Point(0, 1, -1), colors=[None, 'U', 'R']),
       Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
       Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
       Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
       Piece(position=Point(0, 1, 1), colors=[None, 'U', 'L']),
       Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
       Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
       Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
       Piece(position=Point(1, 1, 0), colors=['F', 'U', None]),
       Piece(position=Point(-1, 1, 0), colors=['B', 'U', None]),
       Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
       Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (
              Piece(position=Point(1, 1, -1), colors=['F', 'U', 'R']),
              Piece(position=Point(-1, 1, -1), colors=['B', 'U', 'R']),
              Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
              Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
              Piece(position=Point(1, 1, 1), colors=['F', 'U', 'L']),
              Piece(position=Point(-1, 1, 1), colors=['B', 'U', 'L']),
              Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
              Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_Ui_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Ui()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (Piece(position=Point(1, 1, 0), colors=['R', 'U', None]),
       Piece(position=Point(0, -1, -1), colors=[None, 'D', 'R']),
       Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
       Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
       Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
       Piece(position=Point(0, -1, 1), colors=[None, 'D', 'L']),
       Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
       Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
       Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
       Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
       Piece(position=Point(1, -1, 0), colors=['F', 'D', None]),
       Piece(position=Point(-1, -1, 0), colors=['B', 'D', None]))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, -1), colors=['F', 'D', 'R']),
       Piece(position=Point(-1, -1, -1), colors=['B', 'D', 'R']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['F', 'D', 'L']),
       Piece(position=Point(-1, -1, 1), colors=['B', 'D', 'L']))

      )]
)
def test_D_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.D()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(0, -1, 1), colors=[None, 'D', 'R']),
      Piece(position=Point(1, 0, 1), colors=['R', None, 'F']), Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(0, -1, -1), colors=[None, 'D', 'L']),
      Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
      Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
      Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']), Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
      Piece(position=Point(-1, -1, 0), colors=['F', 'D', None]),
      Piece(position=Point(1, -1, 0), colors=['B', 'D', None]))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['F', 'D', 'R']),
       Piece(position=Point(1, -1, 1), colors=['B', 'D', 'R']), Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, -1), colors=['F', 'D', 'L']),
       Piece(position=Point(1, -1, -1), colors=['B', 'D', 'L']))

      )]
)
def test_Di_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Di()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(0, -1, 1), colors=[None, 'R', 'F']),
      Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(0, 1, 1), colors=[None, 'L', 'F']),
      Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
      Piece(position=Point(1, 0, 1), colors=['U', None, 'F']), Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
      Piece(position=Point(-1, 0, 1), colors=['D', None, 'F']),
      Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(1, -1, 1), colors=['U', 'R', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['D', 'R', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']), Piece(position=Point(1, 1, 1), colors=['U', 'L', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['D', 'L', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_F_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.F()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(0, 1, 1), colors=[None, 'R', 'F']), Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(0, -1, 1), colors=[None, 'L', 'F']),
      Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
      Piece(position=Point(-1, 0, 1), colors=['U', None, 'F']),
      Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']), Piece(position=Point(1, 0, 1), colors=['D', None, 'F']),
      Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(-1, 1, 1), colors=['U', 'R', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, 1, 1), colors=['D', 'R', 'F']), Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['U', 'L', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['D', 'L', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_Fi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Fi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(1, 0, 1), colors=['R', None, 'F']), Piece(position=Point(0, 1, -1), colors=[None, 'R', 'B']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
      Piece(position=Point(0, -1, -1), colors=[None, 'L', 'B']),
      Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
      Piece(position=Point(-1, 0, -1), colors=['U', None, 'B']),
      Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
      Piece(position=Point(1, 0, -1), colors=['D', None, 'B']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(-1, 1, -1), colors=['U', 'R', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']), Piece(position=Point(1, 1, -1), colors=['D', 'R', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['U', 'L', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['D', 'L', 'B']))

      )]
)
def test_B_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.B()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
      Piece(position=Point(0, -1, -1), colors=[None, 'R', 'B']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
      Piece(position=Point(0, 1, -1), colors=[None, 'L', 'B']), Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
      Piece(position=Point(1, 0, -1), colors=['U', None, 'B']),
      Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
      Piece(position=Point(-1, 0, -1), colors=['D', None, 'B']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, -1, -1), colors=['U', 'R', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['D', 'R', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['U', 'L', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['D', 'L', 'B']))

      )]
)
def test_Bi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Bi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'U']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'D']),
       Piece(position=Point(0, -1, 0), colors=[None, 'F', None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'B', None]))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(1, 0, 1), colors=['R', None, 'F']), Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
      Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
      Piece(position=Point(0, -1, 1), colors=[None, 'F', 'U']), Piece(position=Point(0, 1, 1), colors=[None, 'B', 'U']),
      Piece(position=Point(0, -1, -1), colors=[None, 'F', 'D']),
      Piece(position=Point(0, 1, -1), colors=[None, 'B', 'D']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_M_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.M()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'U']),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'D']),
       Piece(position=Point(0, 1, 0), colors=[None, 'F', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'B', None]))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(1, 0, 1), colors=['R', None, 'F']), Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
      Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
      Piece(position=Point(0, 1, -1), colors=[None, 'F', 'U']),
      Piece(position=Point(0, -1, -1), colors=[None, 'B', 'U']),
      Piece(position=Point(0, 1, 1), colors=[None, 'F', 'D']), Piece(position=Point(0, -1, 1), colors=[None, 'B', 'D']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_Mi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.Mi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, 0, -1), colors=[None, None, 'R']),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'L']),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(1, 0, 0), colors=['F', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['B', None, None]))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(1, 0, -1), colors=['F', None, 'R']),
      Piece(position=Point(-1, 0, -1), colors=['B', None, 'R']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(1, 0, 1), colors=['F', None, 'L']), Piece(position=Point(-1, 0, 1), colors=['B', None, 'L']),
      Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']), Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
      Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
      Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_E_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.E()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, 0, 1), colors=[None, None, 'R']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'L']),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(-1, 0, 0), colors=['F', None, None]),
       Piece(position=Point(1, 0, 0), colors=['B', None, None]))
      ,
      (
      Piece(position=Point(1, 1, 0), colors=['R', 'U', None]), Piece(position=Point(1, -1, 0), colors=['R', 'D', None]),
      Piece(position=Point(-1, 0, 1), colors=['F', None, 'R']), Piece(position=Point(1, 0, 1), colors=['B', None, 'R']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'D', None]),
      Piece(position=Point(-1, 0, -1), colors=['F', None, 'L']),
      Piece(position=Point(1, 0, -1), colors=['B', None, 'L']), Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
      Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
      Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
      Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_Ei_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.Ei()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, -1, 0), colors=[None, 'R', None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'L', None]),
       Piece(position=Point(1, 0, 0), colors=['U', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['D', None, None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (Piece(position=Point(1, -1, 0), colors=['U', 'R', None]),
       Piece(position=Point(-1, -1, 0), colors=['D', 'R', None]),
       Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
       Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
       Piece(position=Point(1, 1, 0), colors=['U', 'L', None]),
       Piece(position=Point(-1, 1, 0), colors=['D', 'L', None]),
       Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
       Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
       Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
       Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
       Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
       Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B']))
      ,
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_S_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.S()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, 1, 0), colors=[None, 'R', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'L', None]),
       Piece(position=Point(-1, 0, 0), colors=['U', None, None]),
       Piece(position=Point(1, 0, 0), colors=['D', None, None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
              Piece(position=Point(-1, 1, 0), colors=['U', 'R', None]),
              Piece(position=Point(1, 1, 0), colors=['D', 'R', None]),
              Piece(position=Point(1, 0, 1), colors=['R', None, 'F']),
              Piece(position=Point(1, 0, -1), colors=['R', None, 'B']),
              Piece(position=Point(-1, -1, 0), colors=['U', 'L', None]),
              Piece(position=Point(1, -1, 0), colors=['D', 'L', None]),
              Piece(position=Point(-1, 0, 1), colors=['L', None, 'F']),
              Piece(position=Point(-1, 0, -1), colors=['L', None, 'B']),
              Piece(position=Point(0, 1, 1), colors=[None, 'U', 'F']),
              Piece(position=Point(0, 1, -1), colors=[None, 'U', 'B']),
              Piece(position=Point(0, -1, 1), colors=[None, 'D', 'F']),
              Piece(position=Point(0, -1, -1), colors=[None, 'D', 'B'])),
      (Piece(position=Point(1, 1, 1), colors=['R', 'U', 'F']), Piece(position=Point(1, 1, -1), colors=['R', 'U', 'B']),
       Piece(position=Point(1, -1, 1), colors=['R', 'D', 'F']),
       Piece(position=Point(1, -1, -1), colors=['R', 'D', 'B']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'U', 'F']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'U', 'B']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'D', 'F']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'D', 'B']))

      )]
)
def test_Si_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert cube.corners == expected_corners
    cube.Si()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'U']),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'D']),
       Piece(position=Point(0, 1, 0), colors=[None, 'F', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'B', None]))
      ,
      (
      Piece(position=Point(1, 0, -1), colors=['R', None, 'U']), Piece(position=Point(1, 0, 1), colors=['R', None, 'D']),
      Piece(position=Point(1, 1, 0), colors=['R', 'F', None]), Piece(position=Point(1, -1, 0), colors=['R', 'B', None]),
      Piece(position=Point(-1, 0, -1), colors=['L', None, 'U']),
      Piece(position=Point(-1, 0, 1), colors=['L', None, 'D']),
      Piece(position=Point(-1, 1, 0), colors=['L', 'F', None]),
      Piece(position=Point(-1, -1, 0), colors=['L', 'B', None]),
      Piece(position=Point(0, 1, -1), colors=[None, 'F', 'U']),
      Piece(position=Point(0, -1, -1), colors=[None, 'B', 'U']),
      Piece(position=Point(0, 1, 1), colors=[None, 'F', 'D']), Piece(position=Point(0, -1, 1), colors=[None, 'B', 'D']))
      ,
      (
      Piece(position=Point(1, 1, -1), colors=['R', 'F', 'U']), Piece(position=Point(1, -1, -1), colors=['R', 'B', 'U']),
      Piece(position=Point(1, 1, 1), colors=['R', 'F', 'D']), Piece(position=Point(1, -1, 1), colors=['R', 'B', 'D']),
      Piece(position=Point(-1, 1, -1), colors=['L', 'F', 'U']),
      Piece(position=Point(-1, -1, -1), colors=['L', 'B', 'U']),
      Piece(position=Point(-1, 1, 1), colors=['L', 'F', 'D']), Piece(position=Point(-1, -1, 1), colors=['L', 'B', 'D']))

      )]
)
def test_X_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.X()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(1, 0, 0), colors=['R', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['L', None, None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'U']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'D']),
       Piece(position=Point(0, -1, 0), colors=[None, 'F', None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'B', None]))
      ,
      (
      Piece(position=Point(1, 0, 1), colors=['R', None, 'U']), Piece(position=Point(1, 0, -1), colors=['R', None, 'D']),
      Piece(position=Point(1, -1, 0), colors=['R', 'F', None]), Piece(position=Point(1, 1, 0), colors=['R', 'B', None]),
      Piece(position=Point(-1, 0, 1), colors=['L', None, 'U']),
      Piece(position=Point(-1, 0, -1), colors=['L', None, 'D']),
      Piece(position=Point(-1, -1, 0), colors=['L', 'F', None]),
      Piece(position=Point(-1, 1, 0), colors=['L', 'B', None]),
      Piece(position=Point(0, -1, 1), colors=[None, 'F', 'U']), Piece(position=Point(0, 1, 1), colors=[None, 'B', 'U']),
      Piece(position=Point(0, -1, -1), colors=[None, 'F', 'D']),
      Piece(position=Point(0, 1, -1), colors=[None, 'B', 'D']))
      ,
      (Piece(position=Point(1, -1, 1), colors=['R', 'F', 'U']), Piece(position=Point(1, 1, 1), colors=['R', 'B', 'U']),
       Piece(position=Point(1, -1, -1), colors=['R', 'F', 'D']),
       Piece(position=Point(1, 1, -1), colors=['R', 'B', 'D']),
       Piece(position=Point(-1, -1, 1), colors=['L', 'F', 'U']),
       Piece(position=Point(-1, 1, 1), colors=['L', 'B', 'U']),
       Piece(position=Point(-1, -1, -1), colors=['L', 'F', 'D']),
       Piece(position=Point(-1, 1, -1), colors=['L', 'B', 'D']))
      )]
)
def test_Xi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Xi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, 0, 1), colors=[None, None, 'R']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'L']),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(-1, 0, 0), colors=['F', None, None]),
       Piece(position=Point(1, 0, 0), colors=['B', None, None]))
      ,
      (
      Piece(position=Point(0, 1, 1), colors=[None, 'U', 'R']), Piece(position=Point(0, -1, 1), colors=[None, 'D', 'R']),
      Piece(position=Point(-1, 0, 1), colors=['F', None, 'R']), Piece(position=Point(1, 0, 1), colors=['B', None, 'R']),
      Piece(position=Point(0, 1, -1), colors=[None, 'U', 'L']),
      Piece(position=Point(0, -1, -1), colors=[None, 'D', 'L']),
      Piece(position=Point(-1, 0, -1), colors=['F', None, 'L']),
      Piece(position=Point(1, 0, -1), colors=['B', None, 'L']),
      Piece(position=Point(-1, 1, 0), colors=['F', 'U', None]), Piece(position=Point(1, 1, 0), colors=['B', 'U', None]),
      Piece(position=Point(-1, -1, 0), colors=['F', 'D', None]),
      Piece(position=Point(1, -1, 0), colors=['B', 'D', None]))
      ,
      (Piece(position=Point(-1, 1, 1), colors=['F', 'U', 'R']), Piece(position=Point(1, 1, 1), colors=['B', 'U', 'R']),
       Piece(position=Point(-1, -1, 1), colors=['F', 'D', 'R']),
       Piece(position=Point(1, -1, 1), colors=['B', 'D', 'R']),
       Piece(position=Point(-1, 1, -1), colors=['F', 'U', 'L']),
       Piece(position=Point(1, 1, -1), colors=['B', 'U', 'L']),
       Piece(position=Point(-1, -1, -1), colors=['F', 'D', 'L']),
       Piece(position=Point(1, -1, -1), colors=['B', 'D', 'L']))
      )]
)
def test_Y_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Y()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, 0, -1), colors=[None, None, 'R']),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'L']),
       Piece(position=Point(0, 1, 0), colors=[None, 'U', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'D', None]),
       Piece(position=Point(1, 0, 0), colors=['F', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['B', None, None]))
      ,
      (Piece(position=Point(0, 1, -1), colors=[None, 'U', 'R']),
       Piece(position=Point(0, -1, -1), colors=[None, 'D', 'R']),
       Piece(position=Point(1, 0, -1), colors=['F', None, 'R']),
       Piece(position=Point(-1, 0, -1), colors=['B', None, 'R']),
       Piece(position=Point(0, 1, 1), colors=[None, 'U', 'L']),
       Piece(position=Point(0, -1, 1), colors=[None, 'D', 'L']),
       Piece(position=Point(1, 0, 1), colors=['F', None, 'L']),
       Piece(position=Point(-1, 0, 1), colors=['B', None, 'L']),
       Piece(position=Point(1, 1, 0), colors=['F', 'U', None]),
       Piece(position=Point(-1, 1, 0), colors=['B', 'U', None]),
       Piece(position=Point(1, -1, 0), colors=['F', 'D', None]),
       Piece(position=Point(-1, -1, 0), colors=['B', 'D', None]))
      ,
      (
      Piece(position=Point(1, 1, -1), colors=['F', 'U', 'R']), Piece(position=Point(-1, 1, -1), colors=['B', 'U', 'R']),
      Piece(position=Point(1, -1, -1), colors=['F', 'D', 'R']),
      Piece(position=Point(-1, -1, -1), colors=['B', 'D', 'R']), Piece(position=Point(1, 1, 1), colors=['F', 'U', 'L']),
      Piece(position=Point(-1, 1, 1), colors=['B', 'U', 'L']), Piece(position=Point(1, -1, 1), colors=['F', 'D', 'L']),
      Piece(position=Point(-1, -1, 1), colors=['B', 'D', 'L']))
      )]
)
def test_Yi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Yi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, -1, 0), colors=[None, 'R', None]),
       Piece(position=Point(0, 1, 0), colors=[None, 'L', None]),
       Piece(position=Point(1, 0, 0), colors=['U', None, None]),
       Piece(position=Point(-1, 0, 0), colors=['D', None, None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (Piece(position=Point(1, -1, 0), colors=['U', 'R', None]),
       Piece(position=Point(-1, -1, 0), colors=['D', 'R', None]),
       Piece(position=Point(0, -1, 1), colors=[None, 'R', 'F']),
       Piece(position=Point(0, -1, -1), colors=[None, 'R', 'B']),
       Piece(position=Point(1, 1, 0), colors=['U', 'L', None]),
       Piece(position=Point(-1, 1, 0), colors=['D', 'L', None]),
       Piece(position=Point(0, 1, 1), colors=[None, 'L', 'F']),
       Piece(position=Point(0, 1, -1), colors=[None, 'L', 'B']),
       Piece(position=Point(1, 0, 1), colors=['U', None, 'F']),
       Piece(position=Point(1, 0, -1), colors=['U', None, 'B']),
       Piece(position=Point(-1, 0, 1), colors=['D', None, 'F']),
       Piece(position=Point(-1, 0, -1), colors=['D', None, 'B']))
      ,
      (
      Piece(position=Point(1, -1, 1), colors=['U', 'R', 'F']), Piece(position=Point(1, -1, -1), colors=['U', 'R', 'B']),
      Piece(position=Point(-1, -1, 1), colors=['D', 'R', 'F']),
      Piece(position=Point(-1, -1, -1), colors=['D', 'R', 'B']), Piece(position=Point(1, 1, 1), colors=['U', 'L', 'F']),
      Piece(position=Point(1, 1, -1), colors=['U', 'L', 'B']), Piece(position=Point(-1, 1, 1), colors=['D', 'L', 'F']),
      Piece(position=Point(-1, 1, -1), colors=['D', 'L', 'B']))
      )]
)
def test_Z_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Z()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners


@pytest.mark.parametrize(
    "expected_faces, expected_edges, expected_corners",
    [((Piece(position=Point(0, 1, 0), colors=[None, 'R', None]),
       Piece(position=Point(0, -1, 0), colors=[None, 'L', None]),
       Piece(position=Point(-1, 0, 0), colors=['U', None, None]),
       Piece(position=Point(1, 0, 0), colors=['D', None, None]),
       Piece(position=Point(0, 0, 1), colors=[None, None, 'F']),
       Piece(position=Point(0, 0, -1), colors=[None, None, 'B']))
      ,
      (
      Piece(position=Point(-1, 1, 0), colors=['U', 'R', None]), Piece(position=Point(1, 1, 0), colors=['D', 'R', None]),
      Piece(position=Point(0, 1, 1), colors=[None, 'R', 'F']), Piece(position=Point(0, 1, -1), colors=[None, 'R', 'B']),
      Piece(position=Point(-1, -1, 0), colors=['U', 'L', None]),
      Piece(position=Point(1, -1, 0), colors=['D', 'L', None]),
      Piece(position=Point(0, -1, 1), colors=[None, 'L', 'F']),
      Piece(position=Point(0, -1, -1), colors=[None, 'L', 'B']),
      Piece(position=Point(-1, 0, 1), colors=['U', None, 'F']),
      Piece(position=Point(-1, 0, -1), colors=['U', None, 'B']),
      Piece(position=Point(1, 0, 1), colors=['D', None, 'F']), Piece(position=Point(1, 0, -1), colors=['D', None, 'B']))
      ,
      (
      Piece(position=Point(-1, 1, 1), colors=['U', 'R', 'F']), Piece(position=Point(-1, 1, -1), colors=['U', 'R', 'B']),
      Piece(position=Point(1, 1, 1), colors=['D', 'R', 'F']), Piece(position=Point(1, 1, -1), colors=['D', 'R', 'B']),
      Piece(position=Point(-1, -1, 1), colors=['U', 'L', 'F']),
      Piece(position=Point(-1, -1, -1), colors=['U', 'L', 'B']),
      Piece(position=Point(1, -1, 1), colors=['D', 'L', 'F']), Piece(position=Point(1, -1, -1), colors=['D', 'L', 'B']))
      )]
)
def test_Zi_rotation(expected_faces, expected_edges, expected_corners):
    cube = Cube("UUU"
                "UUU"
                "UUU"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "LLLFFFRRRBBB"
                "DDD"
                "DDD"
                "DDD")
    assert not cube.faces == expected_faces
    assert not cube.edges == expected_edges
    assert not cube.corners == expected_corners
    cube.Zi()
    assert cube.faces == expected_faces
    assert cube.edges == expected_edges
    assert cube.corners == expected_corners
