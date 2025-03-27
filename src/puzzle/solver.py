# src/puzzle/solver.py
from typing import List, Tuple, Optional
import heapq
from copy import deepcopy
from .puzzle_state import PuzzleState
import time
import logging
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, state: PuzzleState, parent: Optional['Node'] = None, move: Optional[Tuple[int, int]] = None):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = 0 if parent is None else parent.g + 1
        self.h = self._calculate_manhattan()
        self.f = self.g + self.h

    @lru_cache(maxsize=None)
    def _calculate_manhattan(self) -> int:
        """Calculate Manhattan distance heuristic."""
        distance = 0
        goal_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
            5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
            9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
            13: (3, 0), 14: (3, 1), 15: (3, 2), 0: (3, 3)
        }

        for i in range(4):
            for j in range(4):
                value = self.state.state[i][j]
                if value != 0:
                    goal_x, goal_y = goal_positions[value]
                    distance += abs(goal_x - i) + abs(goal_y - j)
        return distance

    def __lt__(self, other: 'Node') -> bool:
        return self.f < other.f


class PuzzleSolver:
    def __init__(self, initial_state: PuzzleState):
        self.initial_state = initial_state

    def solve(self) -> Optional[List[Tuple[int, int]]]:
        """Solve the puzzle using A* algorithm"""
        
        logging.info("Checking puzzle solvability")
        if not PuzzleState._is_solvable(self.initial_state.state):
            logging.error("Puzzle is not solvable.")
            raise ValueError("Puzzle is not solvable.")
        
        logging.info("Starting to solve the puzzle")
        start_time = time.time()
        
        start_node = Node(self.initial_state)
        frontier = []
        heapq.heappush(frontier, start_node)
        explored = set()
        
        while frontier:
            current_node = heapq.heappop(frontier)
            logging.info(f"Exploring state: {current_node.state.state}")
            
            if current_node.state.is_goal_state():
                elapsed_time = time.time() - start_time
                logging.info(f"Puzzle solved in {elapsed_time:.2f} seconds")
                return self._reconstruct_path(current_node)
            
            state_str = str(current_node.state.state)
            if state_str in explored:
                continue
                
            explored.add(state_str)
            
            for move in current_node.state.get_possible_moves():
                new_state = PuzzleState(deepcopy(current_node.state.state))
                new_state.move(move)
                
                if str(new_state.state) not in explored:
                    new_node = Node(new_state, current_node, move)
                    heapq.heappush(frontier, new_node)
        
        elapsed_time = time.time() - start_time
        logging.info(f"Failed to solve the puzzle in {elapsed_time:.2f} seconds")
        return None

    def _reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """Reconstruct the path from initial state to goal"""
        path = []
        while node.parent is not None:
            path.append(node.move)
            node = node.parent
        return path[::-1]

    def get_solution_states(self) -> Optional[List[PuzzleState]]:
        """Returns list of states from initial to goal state"""
        moves = self.solve()
        if moves is None:
            return None

        states = [deepcopy(self.initial_state)]
        current_state = deepcopy(self.initial_state)
        
        for move in moves:
            current_state = PuzzleState(deepcopy(current_state.state))
            current_state.move(move)
            states.append(deepcopy(current_state))
            
        return states

