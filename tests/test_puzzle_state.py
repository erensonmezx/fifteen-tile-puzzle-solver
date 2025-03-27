# tests/test_puzzle_state.py
import pytest
from src.puzzle.puzzle_state import PuzzleState

def test_initialization():
    puzzle = PuzzleState()
    assert puzzle.state == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    assert puzzle.blank_position == (3, 3)

def test_possible_moves():
    puzzle = PuzzleState()
    # In goal state, blank is at bottom-right
    # Should only be able to move up or left
    moves = puzzle.get_possible_moves()
    assert len(moves) == 2
    assert (1, 2) in moves  # up
    assert (2, 1) in moves  # left

def test_move():
    puzzle = PuzzleState()
    # Move blank up
    assert puzzle.move((1, 2)) == True
    assert puzzle.state[1][2] == 0
    assert puzzle.state[2][2] == 8

def test_solvability():
    # Test goal state is solvable
    puzzle = PuzzleState()
    assert puzzle._is_solvable() == True
    
    # Test random state generation creates solvable puzzles
    random_puzzle = PuzzleState.create_random_state()
    assert random_puzzle._is_solvable() == True

def test_goal_state_check():
    puzzle = PuzzleState()
    assert puzzle.is_goal_state() == True
    
    puzzle.move((1, 2))  # make a move
    assert puzzle.is_goal_state() == False