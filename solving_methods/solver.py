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
        pass
