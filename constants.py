from game.point import Point
from game.matrix import Matrix

FACE = "face"
EDGE = "edge"
CORNER = "corner"

RIGHT = X_AXIS = Point(1, 0, 0)
LEFT = Point(-1, 0, 0)
UP = Y_AXIS = Point(0, 1, 0)
DOWN = Point(0, -1, 0)
FRONT = Z_AXIS = Point(0, 0, 1)
BACK = Point(0, 0, -1)

# 90 degree rotations in the XY plane. CW is clockwise, CC is counter-clockwise.
ROT_XY_CW = Matrix([0, 1, 0, -1, 0, 0, 0, 0, 1])
ROT_XY_CC = Matrix([0, -1, 0, 1, 0, 0, 0, 0, 1])

# 90 degree rotations in the XZ plane (around the y-axis when viewed pointing toward you).
ROT_XZ_CW = Matrix([0, 0, -1, 0, 1, 0, 1, 0, 0])
ROT_XZ_CC = Matrix([0, 0, 1, 0, 1, 0, -1, 0, 0])

# 90 degree rotations in the YZ plane (around the x-axis when viewed pointing toward you).
ROT_YZ_CW = Matrix([1, 0, 0, 0, 0, 1, 0, -1, 0])
ROT_YZ_CC = Matrix([1, 0, 0, 0, 0, -1, 0, 1, 0])
