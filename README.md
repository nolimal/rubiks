# Rubik's cube

## Introduction

The project contains clean-coded python program to play and solve the Rubik's cube.
It replicates the layer based solving method, which is introduced with some mock-up
examples in the attached PDF.

## Rubik's cube
The cube `(3 * 3 * 3)` consists of `27` pieces - `Cubies`, which has `6` centres, `8` corners and `12` edges.
It allows rotation around `x, y, z` axis. Obviously, centres are fixed and coloured differently. The fronts of `Cubies` are called `Facelets`.

### Move Notations

Define clockwise face rotations:

`F - front, R - right, U - upper,`

` L - left, B - bottom, D - down`

Clockwise slice rotations:

 `M - middle, E - equatorial, S - standing,`

 `X - whole cube around x axis, Y - whole cube around y axis Z - whole cube around z axis`

All anticlockwise rotations are defined with `i` added at the end of the character. 

Here is the link to the interactive API: `https://ruwix.com/the-rubiks-cube/notation/`

### Implementation of the game

#### Piece

Each of the 27 Rubik's pieces can be positioned in the three dimensional Cartesian coordinate system. 
Like that each `Piece` can have its own `position` vector `(x, y, z)` where component is `{-1, 0, 1}`.
Obviously `{0, 0, 0}` is the center of the cube.

Let: 
- `x` axis point in `R`
- `y` axis point in `U`
- `z` axis point in `F`

Each `Piece` has as well `colors` vector `(cx, cy, cz)` with the color of the sticker along each axis.
Obviously only the corner is going to be without any `None` values.

Example:

`colors = ("Orange", None, "Red")` is an edge with orange facing x-direction (`R`) and red facing z-direction (`F`). 

We add private method `rotate` to the class which does a 90-degree rotation. Following the rotation matrix [reference 1]
one can apply a matrix vector multiplication to update position vector. Then we update the colors vector, by swapping exactly two entries in the colors vector.

Example:

`colors = ("Blue", "White", "Red")` defines a corner piece. After rotation is performed one sticker will remain facing the same axis, whereas the other two stickers swap axes.
This implies swapping the position of two entries in the `colors` vector.

#### Cube

The `Cube` stores a list of `Pieces`, methods to flip the slices and queries to obtain current state. Rotation matrix multiplication is encapsulated in previous class `Piece`.
This simplifies rotation of the cube, by applying the rotation matrix to `Pieces` affected by the rotation.

Example:

To apply `.R` rotation of the right face we must do the following:

- Create rotation matrix for 90 - degree rotation in the `x = 1` plane
- Select `Pieces` with `position.x == 1`
- Apply the rotation matrix to the selected `Pieces`.

#### Layer based algorithm

In implementation vocabulary we first solve
`F` face (`z = 1`), then `M` layer (`z = 0`) and then `D`or back layer (`z = -1`).

When the algorithm finishes, the `Solver.moves` shows the list representing solution sequence.

### References

[1] Robert C. Martin: Clean Code: A Handbook of Agile Software Craftsmanship (2008) p. 122-133

[2] Beginner Solution to the Rubik's Cube (2005) p. 1-7

[3] Rotation matrix https://en.wikipedia.org/wiki/Rotation_matrix

