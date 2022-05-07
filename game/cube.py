from __future__ import annotations

from game.piece import Piece
from game.point import Point
from constants import (
    RIGHT,
    LEFT,
    UP,
    DOWN,
    FRONT,
    FACE,
    BACK,
    CORNER,
    ROT_XY_CW,
    ROT_XY_CC,
    ROT_XZ_CW,
    ROT_XZ_CC,
    ROT_YZ_CW,
    ROT_YZ_CC,
    EDGE,
    X_AXIS,
    Y_AXIS,
    Z_AXIS,
)
import string
from dataclasses import dataclass
from typing import Tuple, Union, Optional, List


@dataclass
class Cube:
    """Stores Pieces which are addressed through an x-y-z coordinate system:
    -x is the LEFT direction, +x is the RIGHT direction
    -y is the DOWN direction, +y is the UP direction
    -z is the BACK direction, +z is the FRONT direction
    """

    cube_str: Union[str, Cube]
    faces: Optional[Tuple, List] = None
    edges: Optional[Tuple, List] = None
    corners: Optional[Tuple, List] = None
    pieces: Optional[Tuple, List] = None

    def __post_init__(self):
        """
        cube_str looks like:
                UUU                       0  1  2
                UUU                       3  4  5
                UUU                       6  7  8
            LLL FFF RRR BBB      9 10 11 12 13 14 15 16 17 18 19 20
            LLL FFF RRR BBB     21 22 23 24 25 26 27 28 29 30 31 32
            LLL FFF RRR BBB     33 34 35 36 37 38 39 40 41 42 43 44
                DDD                      45 46 47
                DDD                      48 49 50
                DDD                      51 52 53
        Note that the back side is mirrored in the horizontal axis
        during unfolding.
        Each 'sticker' must be a single character.
        """
        if isinstance(self.cube_str, Cube):
            self._from_cube(self.cube_str)
            return

        cube_str = "".join(
            x for x in self.cube_str if x not in string.whitespace
        )
        assert len(cube_str) == 54
        self._set_faces()
        self._set_edges()
        self._set_corners()
        self._set_pieces()
        self._assert_data()

    def _set_faces(self):
        self.faces = (
            Piece(position=RIGHT, colors=(self.cube_str[28], None, None)),
            Piece(position=LEFT, colors=(self.cube_str[22], None, None)),
            Piece(position=UP, colors=(None, self.cube_str[4], None)),
            Piece(position=DOWN, colors=(None, self.cube_str[49], None)),
            Piece(position=FRONT, colors=(None, None, self.cube_str[25])),
            Piece(position=BACK, colors=(None, None, self.cube_str[31])),
        )

    def _set_edges(self):
        self.edges = (
            Piece(
                position=RIGHT + UP,
                colors=(self.cube_str[16], self.cube_str[5], None),
            ),
            Piece(
                position=RIGHT + DOWN,
                colors=(self.cube_str[40], self.cube_str[50], None),
            ),
            Piece(
                position=RIGHT + FRONT,
                colors=(self.cube_str[27], None, self.cube_str[26]),
            ),
            Piece(
                position=RIGHT + BACK,
                colors=(self.cube_str[29], None, self.cube_str[30]),
            ),
            Piece(
                position=LEFT + UP,
                colors=(self.cube_str[10], self.cube_str[3], None),
            ),
            Piece(
                position=LEFT + DOWN,
                colors=(self.cube_str[34], self.cube_str[48], None),
            ),
            Piece(
                position=LEFT + FRONT,
                colors=(self.cube_str[23], None, self.cube_str[24]),
            ),
            Piece(
                position=LEFT + BACK,
                colors=(self.cube_str[21], None, self.cube_str[32]),
            ),
            Piece(
                position=UP + FRONT,
                colors=(None, self.cube_str[7], self.cube_str[13]),
            ),
            Piece(
                position=UP + BACK,
                colors=(None, self.cube_str[1], self.cube_str[19]),
            ),
            Piece(
                position=DOWN + FRONT,
                colors=(None, self.cube_str[46], self.cube_str[37]),
            ),
            Piece(
                position=DOWN + BACK,
                colors=(None, self.cube_str[52], self.cube_str[43]),
            ),
        )

    def _set_corners(self):
        self.corners = (
            Piece(
                position=RIGHT + UP + FRONT,
                colors=(
                    self.cube_str[15],
                    self.cube_str[8],
                    self.cube_str[14],
                ),
            ),
            Piece(
                position=RIGHT + UP + BACK,
                colors=(
                    self.cube_str[17],
                    self.cube_str[2],
                    self.cube_str[18],
                ),
            ),
            Piece(
                position=RIGHT + DOWN + FRONT,
                colors=(
                    self.cube_str[39],
                    self.cube_str[47],
                    self.cube_str[38],
                ),
            ),
            Piece(
                position=RIGHT + DOWN + BACK,
                colors=(
                    self.cube_str[41],
                    self.cube_str[53],
                    self.cube_str[42],
                ),
            ),
            Piece(
                position=LEFT + UP + FRONT,
                colors=(
                    self.cube_str[11],
                    self.cube_str[6],
                    self.cube_str[12],
                ),
            ),
            Piece(
                position=LEFT + UP + BACK,
                colors=(self.cube_str[9], self.cube_str[0], self.cube_str[20]),
            ),
            Piece(
                position=LEFT + DOWN + FRONT,
                colors=(
                    self.cube_str[35],
                    self.cube_str[45],
                    self.cube_str[36],
                ),
            ),
            Piece(
                position=LEFT + DOWN + BACK,
                colors=(
                    self.cube_str[33],
                    self.cube_str[51],
                    self.cube_str[44],
                ),
            ),
        )

    def _set_pieces(self):
        self.pieces = self.faces + self.edges + self.corners

    def _assert_data(self):
        assert len(self.pieces) == 26
        assert all(p.type == FACE for p in self.faces)
        assert all(p.type == EDGE for p in self.edges)
        assert all(p.type == CORNER for p in self.corners)

    def _from_cube(self, c):
        self.faces = [
            Piece(position=Point(p.position), colors=p.colors) for p in c.faces
        ]
        self.edges = [
            Piece(position=Point(p.position), colors=p.colors) for p in c.edges
        ]
        self.corners = [
            Piece(position=Point(p.position), colors=p.colors)
            for p in c.corners
        ]
        self.pieces = self.faces + self.edges + self.corners
        self._assert_data()

    def is_solved(self):
        def check(colors):
            assert len(colors) == 9
            return all(c == colors[0] for c in colors)

        return (
                check([piece.colors[2] for piece in self._face(FRONT)])
                and check([piece.colors[2] for piece in self._face(BACK)])
                and check([piece.colors[1] for piece in self._face(UP)])
                and check([piece.colors[1] for piece in self._face(DOWN)])
                and check([piece.colors[0] for piece in self._face(LEFT)])
                and check([piece.colors[0] for piece in self._face(RIGHT)])
        )

    def _face(self, axis):
        """
        :param axis: One of FRONT, BACK, UP, DOWN, LEFT, RIGHT
        :return: A list of Pieces on the given face
        """
        assert axis.count(0) == 2
        return [p for p in self.pieces if p.position.dot(axis) > 0]

    def _slice(self, plane):
        """
        :param plane: A sum of any two of X_AXIS, Y_AXIS, Z_AXIS
        (e.g. X_AXIS + Y_AXIS)
        :return: A list of Pieces in the given plane
        """
        assert plane.count(0) == 1
        i = next((i for i, x in enumerate(plane) if x == 0))
        return [p for p in self.pieces if p.position[i] == 0]

    def _rotate_face(self, face, matrix):
        self._rotate_pieces(self._face(face), matrix)

    def _rotate_slice(self, plane, matrix):
        self._rotate_pieces(self._slice(plane), matrix)

    @staticmethod
    def _rotate_pieces(pieces, matrix):
        for piece in pieces:
            piece.rotate(matrix)

    def L(self):
        self._rotate_face(LEFT, ROT_YZ_CC)

    def Li(self):
        self._rotate_face(LEFT, ROT_YZ_CW)

    def R(self):
        self._rotate_face(RIGHT, ROT_YZ_CW)

    def Ri(self):
        self._rotate_face(RIGHT, ROT_YZ_CC)

    def U(self):
        self._rotate_face(UP, ROT_XZ_CW)

    def Ui(self):
        self._rotate_face(UP, ROT_XZ_CC)

    def D(self):
        self._rotate_face(DOWN, ROT_XZ_CC)

    def Di(self):
        self._rotate_face(DOWN, ROT_XZ_CW)

    def F(self):
        self._rotate_face(FRONT, ROT_XY_CW)

    def Fi(self):
        self._rotate_face(FRONT, ROT_XY_CC)

    def B(self):
        self._rotate_face(BACK, ROT_XY_CC)

    def Bi(self):
        self._rotate_face(BACK, ROT_XY_CW)

    def M(self):
        self._rotate_slice(Y_AXIS + Z_AXIS, ROT_YZ_CC)

    def Mi(self):
        self._rotate_slice(Y_AXIS + Z_AXIS, ROT_YZ_CW)

    def E(self):
        self._rotate_slice(X_AXIS + Z_AXIS, ROT_XZ_CC)

    def Ei(self):
        self._rotate_slice(X_AXIS + Z_AXIS, ROT_XZ_CW)

    def S(self):
        self._rotate_slice(X_AXIS + Y_AXIS, ROT_XY_CW)

    def Si(self):
        self._rotate_slice(X_AXIS + Y_AXIS, ROT_XY_CC)

    def X(self):
        self._rotate_pieces(self.pieces, ROT_YZ_CW)

    def Xi(self):
        self._rotate_pieces(self.pieces, ROT_YZ_CC)

    def Y(self):
        self._rotate_pieces(self.pieces, ROT_XZ_CW)

    def Yi(self):
        self._rotate_pieces(self.pieces, ROT_XZ_CC)

    def Z(self):
        self._rotate_pieces(self.pieces, ROT_XY_CW)

    def Zi(self):
        self._rotate_pieces(self.pieces, ROT_XY_CC)

    def sequence(self, move_str):
        """
        :param move_str:
        :param moves: A string containing notated moves separated by spaces:
        "L Ri U M Ui B M"
        """
        moves = [getattr(self, name) for name in move_str.split()]
        for move in moves:
            move()

    def find_piece(self, *colors):
        if None in colors:
            return
        for p in self.pieces:
            if p.colors.count(None) == 3 - len(colors) and all(
                    c in p.colors for c in colors
            ):
                return p

    def get_piece(self, x, y, z):
        """
        :return: the Piece at the given Point
        """
        point = Point(x, y, z)
        for p in self.pieces:
            if p.position == point:
                return p

    def __getitem__(self, *args):
        if len(args) == 1:
            return self.get_piece(*args[0])
        return self.get_piece(*args)

    def __eq__(self, other):
        return (
                isinstance(other, Cube)
                and self._color_list() == other._color_list()
        )

    def __ne__(self, other):
        return not (self == other)

    def colors(self):
        """
        :return: A set containing the colors of all stickers on the cube
        """
        return set(
            c for piece in self.pieces for c in piece.colors if c is not None
        )

    def left_color(self):
        return self[LEFT].colors[0]

    def right_color(self):
        return self[RIGHT].colors[0]

    def up_color(self):
        return self[UP].colors[1]

    def down_color(self):
        return self[DOWN].colors[1]

    def front_color(self):
        return self[FRONT].colors[2]

    def back_color(self):
        return self[BACK].colors[2]

    def _color_list(self):
        right = [
            p.colors[0]
            for p in sorted(
                self._face(RIGHT), key=lambda p: (-p.position.y, -p.position.z)
            )
        ]
        left = [
            p.colors[0]
            for p in sorted(
                self._face(LEFT), key=lambda p: (-p.position.y, p.position.z)
            )
        ]
        up = [
            p.colors[1]
            for p in sorted(
                self._face(UP), key=lambda p: (p.position.z, p.position.x)
            )
        ]
        down = [
            p.colors[1]
            for p in sorted(
                self._face(DOWN), key=lambda p: (-p.position.z, p.position.x)
            )
        ]
        front = [
            p.colors[2]
            for p in sorted(
                self._face(FRONT), key=lambda p: (-p.position.y, p.position.x)
            )
        ]
        back = [
            p.colors[2]
            for p in sorted(
                self._face(BACK), key=lambda p: (-p.position.y, -p.position.x)
            )
        ]

        return (
                up
                + left[0:3]
                + front[0:3]
                + right[0:3]
                + back[0:3]
                + left[3:6]
                + front[3:6]
                + right[3:6]
                + back[3:6]
                + left[6:9]
                + front[6:9]
                + right[6:9]
                + back[6:9]
                + down
        )

    def flat_str(self):
        return "".join(x for x in str(self) if x not in string.whitespace)

    def __str__(self):
        template = (
            "    {}{}{}\n"
            "    {}{}{}\n"
            "    {}{}{}\n"
            "{}{}{} {}{}{} {}{}{} {}{}{}\n"
            "{}{}{} {}{}{} {}{}{} {}{}{}\n"
            "{}{}{} {}{}{} {}{}{} {}{}{}\n"
            "    {}{}{}\n"
            "    {}{}{}\n"
            "    {}{}{}"
        )

        return "    " + template.format(*self._color_list()).strip()
