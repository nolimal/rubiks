from constants import RIGHT, LEFT, UP, DOWN, FRONT, BACK


def get_rotations_from_face(face):
    """
    :param face: One of FRONT, BACK, LEFT, RIGHT, UP, DOWN
    :return: A pair (CW, CC) given the clockwise and counterclockwise
    rotations for that face
    """
    if face == RIGHT:
        return "R", "Ri"
    elif face == LEFT:
        return "L", "Li"
    elif face == UP:
        return "U", "Ui"
    elif face == DOWN:
        return "D", "Di"
    elif face == FRONT:
        return "F", "Fi"
    elif face == BACK:
        return "B", "Bi"
    return None
