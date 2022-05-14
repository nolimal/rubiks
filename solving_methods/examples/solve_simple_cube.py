from game.cube import Cube
from solving_methods.solver import Solver

c = Cube("DLURRDFFUBBLDDRBRBLDLRBFRUULFBDDUFBRBBRFUDFLUDLUULFLFR")
print("Solving cube:\n", c)
orig = Cube(c)
solver = Solver(c)
solver.solve()
assert solver.cube.is_solved()

print(f"{len(solver.moves)} moves: {' '.join(solver.moves)}")

check = Cube(orig)
check.sequence(" ".join(solver.moves))
assert check.is_solved()
