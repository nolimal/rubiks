from constants import DOWN
from constants import LEFT
from constants import RIGHT
from constants import UP
from game.point import Point
from solving_methods.utilities import get_rotations_from_face

DEBUG = False


class Solver:
    def __init__(self, cube):
        self.cube = cube
        self.colors = cube.colors()
        self.moves = []

        self.left_piece = self.cube.find_piece(self.cube.left_color())
        self.right_piece = self.cube.find_piece(self.cube.right_color())
        self.up_piece = self.cube.find_piece(self.cube.up_color())
        self.down_piece = self.cube.find_piece(self.cube.down_color())

    def solve(self):
        if DEBUG:
            print(self.cube)
        self.cross()

    def move(self, move_str):
        self.moves.extend(move_str.split())
        self.cube.sequence(move_str)

    def cross(self):
        if DEBUG:
            print("cross")
        # place the UP-LEFT piece
        fl_piece = self.cube.find_piece(
            self.cube.front_color(), self.cube.left_color()
        )
        fr_piece = self.cube.find_piece(
            self.cube.front_color(), self.cube.right_color()
        )
        fu_piece = self.cube.find_piece(
            self.cube.front_color(), self.cube.up_color()
        )
        fd_piece = self.cube.find_piece(
            self.cube.front_color(), self.cube.down_color()
        )

        self._cross_left_or_right(
            fl_piece,
            self.left_piece,
            self.cube.left_color(),
            "L L",
            "E L Ei Li",
        )
        self._cross_left_or_right(
            fr_piece,
            self.right_piece,
            self.cube.right_color(),
            "R R",
            "Ei R E Ri",
        )

        self.move("Z")
        self._cross_left_or_right(
            fd_piece,
            self.down_piece,
            self.cube.left_color(),
            "L L",
            "E L Ei Li",
        )
        self._cross_left_or_right(
            fu_piece,
            self.up_piece,
            self.cube.right_color(),
            "R R",
            "Ei R E Ri",
        )
        self.move("Zi")

    def _cross_left_or_right(
            self, edge_piece, face_piece, face_color, move_1, move_2
    ):
        # don't do anything if piece is in correct place
        if (
                edge_piece.position
                == (face_piece.position.x, face_piece.position.y, 1)
                and edge_piece.colors[2] == self.cube.front_color()
        ):
            return

        # ensure piece is at z = -1
        undo_move = None
        if edge_piece.position.z == 0:
            pos = Point(edge_piece.position)
            pos.x = 0  # pick the UP or DOWN face
            cw, cc = get_rotations_from_face(pos)

            if edge_piece.position in (LEFT + UP, RIGHT + DOWN):
                self.move(cw)
                undo_move = cc
            else:
                self.move(cc)
                undo_move = cw
        elif edge_piece.position.z == 1:
            pos = Point(edge_piece.position)
            pos.z = 0
            cw, cc = get_rotations_from_face(pos)
            self.move("{0} {0}".format(cc))
            # don't set the undo move if the piece starts
            # out in the right position
            # (with wrong orientation) or we'll screw up the remainder
            # of the algorithm
            if edge_piece.position.x != face_piece.position.x:
                undo_move = "{0} {0}".format(cw)

        assert edge_piece.position.z == -1

        # piece is at z = -1, rotate to correct face (LEFT or RIGHT)
        count = 0
        while (edge_piece.position.x, edge_piece.position.y) != (
                face_piece.position.x,
                face_piece.position.y,
        ):
            self.move("B")
            count += 1
            if count == 10:
                raise Exception(
                    "Stuck in loop - unsolvable cube?\n" + str(self.cube)
                )

        # if we moved a correctly-placed piece, restore it
        if undo_move:
            self.move(undo_move)

        # the piece is on the correct face on plane z = -1,
        # but has two orientations
        if edge_piece.colors[0] == face_color:
            self.move(move_1)
        else:
            self.move(move_2)

    def cross_corners(self):
        if DEBUG:
            print("cross_corners")
        fld_piece = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.left_color(),
            self.cube.down_color(),
        )
        flu_piece = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.left_color(),
            self.cube.up_color(),
        )
        frd_piece = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.right_color(),
            self.cube.down_color(),
        )
        fru_piece = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.right_color(),
            self.cube.up_color(),
        )

        self.place_frd_corner(
            frd_piece,
            self.right_piece,
            self.down_piece,
            self.cube.front_color(),
        )
        self.move("Z")
        self.place_frd_corner(
            fru_piece, self.up_piece, self.right_piece, self.cube.front_color()
        )
        self.move("Z")
        self.place_frd_corner(
            flu_piece, self.left_piece, self.up_piece, self.cube.front_color()
        )
        self.move("Z")
        self.place_frd_corner(
            fld_piece,
            self.down_piece,
            self.left_piece,
            self.cube.front_color(),
        )
        self.move("Z")

    def place_frd_corner(
            self, corner_piece, right_piece, down_piece, front_color
    ):
        # rotate to z = -1
        if corner_piece.position.z == 1:
            pos = Point(corner_piece.position)
            pos.x = pos.z = 0
            cw, cc = get_rotations_from_face(pos)

            # be careful not to screw up other pieces on the front face
            count = 0
            undo_move = cc
            while corner_piece.position.z != -1:
                self.move(cw)
                count += 1

            if count > 1:
                # go the other direction because I don't know which is which.
                # we need to do only one flip (net) or we'll move other
                # correctly-placed corners out of place.
                for _ in range(count):
                    self.move(cc)

                count = 0
                while corner_piece.position.z != -1:
                    self.move(cc)
                    count += 1
                undo_move = cw
            self.move("B")
            for _ in range(count):
                self.move(undo_move)

        # rotate piece to be directly below its destination
        while (corner_piece.position.x, corner_piece.position.y) != (
                right_piece.position.x,
                down_piece.position.y,
        ):
            self.move("B")

        # there are three possible orientations for a corner
        if corner_piece.colors[0] == front_color:
            self.move("B D Bi Di")
        elif corner_piece.colors[1] == front_color:
            self.move("Bi Ri B R")
        else:
            self.move("Ri B B R Bi Bi D Bi Di")

    def second_layer(self):
        rd_piece = self.cube.find_piece(
            self.cube.right_color(), self.cube.down_color()
        )
        ru_piece = self.cube.find_piece(
            self.cube.right_color(), self.cube.up_color()
        )
        ld_piece = self.cube.find_piece(
            self.cube.left_color(), self.cube.down_color()
        )
        lu_piece = self.cube.find_piece(
            self.cube.left_color(), self.cube.up_color()
        )

        self.place_middle_layer_ld_edge(
            ld_piece, self.cube.left_color(), self.cube.down_color()
        )
        self.move("Z")
        self.place_middle_layer_ld_edge(
            rd_piece, self.cube.left_color(), self.cube.down_color()
        )
        self.move("Z")
        self.place_middle_layer_ld_edge(
            ru_piece, self.cube.left_color(), self.cube.down_color()
        )
        self.move("Z")
        self.place_middle_layer_ld_edge(
            lu_piece, self.cube.left_color(), self.cube.down_color()
        )
        self.move("Z")

    def place_middle_layer_ld_edge(self, ld_piece, left_color, down_color):
        # move to z == -1
        if ld_piece.position.z == 0:
            count = 0
            while (ld_piece.position.x, ld_piece.position.y) != (-1, -1):
                self.move("Z")
                count += 1

            self.move("B L Bi Li Bi Di B D")
            for _ in range(count):
                self.move("Zi")

        assert ld_piece.position.z == -1

        if ld_piece.colors[2] == left_color:
            # left_color is on the back face, move piece to down face
            while ld_piece.position.y != -1:
                self.move("B")
            self.move("B L Bi Li Bi Di B D")
        elif ld_piece.colors[2] == down_color:
            # down_color is on the back face, move to left face
            while ld_piece.position.x != -1:
                self.move("B")
            self.move("Bi Di B D B L Bi Li")
        else:
            raise Exception("BUG!!")

    def back_face_edges(self):
        # rotate BACK to FRONT
        self.move("X X")

        # States:  1     2     3     4
        #         -B-   -B-   ---   ---
        #         BBB   BB-   BBB   -B-
        #         -B-   ---   ---   ---
        def state1():
            return (
                    self.cube[0, 1, 1].colors[2] == self.cube.front_color()
                    and self.cube[-1, 0, 1].colors[2] == self.cube.front_color()
                    and self.cube[0, -1, 1].colors[2] == self.cube.front_color()
                    and self.cube[1, 0, 1].colors[2] == self.cube.front_color()
            )

        def state2():
            return (
                    self.cube[0, 1, 1].colors[2] == self.cube.front_color()
                    and self.cube[-1, 0, 1].colors[2] == self.cube.front_color()
            )

        def state3():
            return (
                    self.cube[-1, 0, 1].colors[2] == self.cube.front_color()
                    and self.cube[1, 0, 1].colors[2] == self.cube.front_color()
            )

        def state4():
            return (
                    self.cube[0, 1, 1].colors[2] != self.cube.front_color()
                    and self.cube[-1, 0, 1].colors[2] != self.cube.front_color()
                    and self.cube[0, -1, 1].colors[2] != self.cube.front_color()
                    and self.cube[1, 0, 1].colors[2] != self.cube.front_color()
            )

        count = 0
        while not state1():
            if state4() or state2():
                self.move("D F R Fi Ri Di")
            elif state3():
                self.move("D R F Ri Fi Di")
            else:
                self.move("F")
            count += 1
            if count == 10:
                raise Exception(
                    "Stuck in loop - unsolvable cube\n" + str(self.cube)
                )

        self.move("Xi Xi")

    def last_layer_corners_position(self):
        self.move("X X")
        # UP face:
        #  4-3
        #  ---
        #  2-1
        move_1 = "Li Fi L D F Di Li F L F F "  # swaps 1 and 2
        move_2 = "F Li Fi L D F Di Li F L F "  # swaps 1 and 3

        c1 = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.right_color(),
            self.cube.down_color(),
        )
        c2 = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.left_color(),
            self.cube.down_color(),
        )
        c3 = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.right_color(),
            self.cube.up_color(),
        )
        c4 = self.cube.find_piece(
            self.cube.front_color(),
            self.cube.left_color(),
            self.cube.up_color(),
        )

        # place corner 4
        if c4.position == Point(1, -1, 1):
            self.move(move_1 + "Zi " + move_1 + " Z")
        elif c4.position == Point(1, 1, 1):
            self.move("Z " + move_2 + " Zi")
        elif c4.position == Point(-1, -1, 1):
            self.move("Zi " + move_1 + " Z")
        assert c4.position == Point(-1, 1, 1)

        # place corner 2
        if c2.position == Point(1, 1, 1):
            self.move(move_2 + move_1)
        elif c2.position == Point(1, -1, 1):
            self.move(move_1)
        assert c2.position == Point(-1, -1, 1)

        # place corner 3 and corner 1
        if c3.position == Point(1, -1, 1):
            self.move(move_2)
        assert c3.position == Point(1, 1, 1)
        assert c1.position == Point(1, -1, 1)

        self.move("Xi Xi")
