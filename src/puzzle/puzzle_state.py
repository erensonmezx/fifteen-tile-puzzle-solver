"""
PuzzleState Class
-----------------
This module defines the PuzzleState class, which represents the state of the 8-puzzle game.
It includes methods for checking solvability, moving tiles, and determining the goal state.
"""
# src/puzzle/puzzle_state.py
from typing import List, Tuple, Optional
import random
import logging

logging.basicConfig(level=logging.INFO)
class PuzzleState:
    def __init__(self, state: Optional[List[List[int]]] = None):
        self.size = 4
        self.state = state if state else self._create_goal_state()
        self.blank_position = self._find_blank()

    def _create_goal_state(self) -> List[List[int]]:
        
        state = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]  # 0 represents the blank tile
        ]
        return state

    def _find_blank(self) -> Tuple[int, int]:
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 0:
                    return (i, j)
        raise ValueError("Invalid puzzle state: no blank tile found")
        
    @staticmethod
    def _is_solvable(state: List[List[int]]) -> bool:
        """Checks if a puzzle state is solvable."""
        # Flatten the state into a 1D list
        tiles = [tile for row in state for tile in row if tile != 0]

        # Count inversions
        inversions = 0
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1

        # Find the row of the blank tile (0)
        blank_row = next(i for i, row in enumerate(state) if 0 in row)

        # For 4x4 grids:
        # - If the blank is on an even row from the bottom (0-indexed), inversions must be odd
        # - If the blank is on an odd row from the bottom, inversions must be even
        return (inversions % 2 == 0) if (3 - blank_row) % 2 == 0 else (inversions % 2 != 0)
    
    def is_solvable(self) -> bool:
        """Check if the current puzzle state is solvable."""
        return self._is_solvable(self.state)


    @staticmethod
    def create_random_state() -> 'PuzzleState':
        """Creates a random solvable puzzle state using Fisher-Yates shuffle."""
        while True:
            # Flatten the goal state into a 1D list
            tiles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
            random.shuffle(tiles)  # Shuffle the tiles

            # Convert back to a 4x4 grid
            state = [tiles[i:i + 4] for i in range(0, 16, 4)]

            # Check if the shuffled state is solvable
            if PuzzleState._is_solvable(state):
                break

        # Create and return the PuzzleState object
        return PuzzleState(state)

    # @staticmethod
    # def create_random_state() -> 'PuzzleState':
    #     """Creates a random solvable puzzle state using random walk from goal state."""
    #     current = PuzzleState()
    #     moves = random.randint(50, 100)  # Increase the range for more shuffling
    #     last_move = None

    #     for _ in range(moves):
    #         possible_moves = current.get_possible_moves()
    #         if last_move:
    #             # Exclude the reverse of the last move
    #             reverse_move = (last_move[0] * -1, last_move[1] * -1)
    #             possible_moves = [move for move in possible_moves if move != reverse_move]

    #         if possible_moves:
    #             move = random.choice(possible_moves)
    #             current.move(move)
    #             # Calculate the direction of the move
    #             x, y = current.blank_position
    #             last_move = (x - move[0], y - move[1])  # Update last move
    #     return current

    def get_possible_moves(self) -> List[Tuple[int, int]]:
        """Returns list of possible moves from current state"""
        moves = []
        x, y = self.blank_position
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 4 and 0 <= new_y < 4:  # Change from 3 to 4
                moves.append((new_x, new_y))
        return moves

    def move(self, position: Tuple[int, int]) -> bool:
        """Makes a move by swapping blank with given position"""
        if position not in self.get_possible_moves():
            return False
        
        new_x, new_y = position
        x, y = self.blank_position
        
        self.state[x][y], self.state[new_x][new_y] = self.state[new_x][new_y], self.state[x][y]
        self.blank_position = (new_x, new_y)
        return True

    def is_goal_state(self) -> bool:
        """Checks if current state is goal state"""
        goal = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        return self.state == goal

    def __str__(self) -> str:
        """String representation of puzzle state"""
        return '\n'.join(' '.join(str(x) for x in row) for row in self.state)

    def __eq__(self, other: 'PuzzleState') -> bool:
        """Checks if two puzzle states are equal"""
        if not isinstance(other, PuzzleState):
            return False
        return self.state == other.state

    def __hash__(self) -> int:
        """Generates hash of puzzle state for use in sets/dicts"""
        return hash(str(self.state))