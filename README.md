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

### Layer based algorithm

