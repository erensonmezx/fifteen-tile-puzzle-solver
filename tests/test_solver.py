import pytest
from src.puzzle.puzzle_state import PuzzleState
from src.puzzle.solver import PuzzleSolver

def test_solver_with_goal_state():
    puzzle = PuzzleState()
    solver = PuzzleSolver(puzzle)
    solution = solver.solve()
    assert solution == []  # Already in goal state

def test_solver_with_unsolvable_state():
    unsolvable_state = PuzzleState([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 15, 14, 0]])
    solver = PuzzleSolver(unsolvable_state)
    with pytest.raises(ValueError, match="Puzzle is not solvable."):
        solver.solve()

def test_solver_with_random_state():
    puzzle = PuzzleState.create_random_state()
    solver = PuzzleSolver(puzzle)
    solution = solver.solve()
    assert solution is not None
    assert puzzle.is_goal_state()  # Solution leads to goal state