import time
import copy
from board import Board
from rules import get_valid_moves, get_valid_arrows
from typing import Tuple, List

class IterativeAgent:
    def __init__(self, agent_id: int, time_limit: float = 2.0, max_depth: int = 5):
        self.agent_id = agent_id
        self.time_limit = time_limit
        self.max_depth = max_depth

    def get_action(self, board: Board) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        self.start_time = time.time()
        best_action = None

        for depth in range(1, self.max_depth + 1):
            try:
                action = self.search_at_depth(board, depth)
                if time.time() - self.start_time < self.time_limit:
                    best_action = action
                else:
                    break
            except TimeoutError:
                break

        if best_action:
            return best_action
        raise ValueError("No valid moves found within time limit")

    def search_at_depth(self, board: Board, depth: int):
        pos_list = board.agent_1_pos if self.agent_id == 1 else board.agent_2_pos
        best_score = float('-inf')
        best_action = None

        for from_pos in pos_list:
            for to_pos in get_valid_moves(board, from_pos):
                for arrow_pos in get_valid_arrows(board, to_pos):
                    if time.time() - self.start_time > self.time_limit:
                        raise TimeoutError

                    board_copy = copy.deepcopy(board)
                    board_copy.move(from_pos, to_pos, self.agent_id)
                    board_copy.arrow_place(from_pos, arrow_pos, self.agent_id)
                    board_copy.update_temp_blocks()

                    score = self.minimax(board_copy, depth - 1, False)
                    if score > best_score:
                        best_score = score
                        best_action = (from_pos, to_pos, arrow_pos)

        return best_action

    def minimax(self, board: Board, depth: int, maximizing: bool) -> float:
        if depth == 0 or time.time() - self.start_time > self.time_limit:
            return self.board_eval(board)

        current_agent_id = self.agent_id if maximizing else 3 - self.agent_id
        pos_list = board.agent_1_pos if current_agent_id == 1 else board.agent_2_pos

        if maximizing:
            best = float('-inf')
            for from_pos in pos_list:
                for to_pos in get_valid_moves(board, from_pos):
                    for arrow_pos in get_valid_arrows(board, to_pos):
                        if time.time() - self.start_time > self.time_limit:
                            raise TimeoutError
                        board_copy = copy.deepcopy(board)
                        board_copy.move(from_pos, to_pos, current_agent_id)
                        board_copy.arrow_place(from_pos, arrow_pos, current_agent_id)
                        board_copy.update_temp_blocks()
                        score = self.minimax(board_copy, depth - 1, False)
                        best = max(best, score)
            return best
        else:
            best = float('inf')
            for from_pos in pos_list:
                for to_pos in get_valid_moves(board, from_pos):
                    for arrow_pos in get_valid_arrows(board, to_pos):
                        if time.time() - self.start_time > self.time_limit:
                            raise TimeoutError
                        board_copy = copy.deepcopy(board)
                        board_copy.move(from_pos, to_pos, current_agent_id)
                        board_copy.arrow_place(from_pos, arrow_pos, current_agent_id)
                        board_copy.update_temp_blocks()
                        score = self.minimax(board_copy, depth - 1, True)
                        best = min(best, score)
            return best

    def board_eval(self, board: Board) -> float:
        my_pos = board.agent_1_pos if self.agent_id == 1 else board.agent_2_pos
        opp_pos = board.agent_2_pos if self.agent_id == 1 else board.agent_1_pos

        my_mob = sum(len(get_valid_moves(board, pos)) for pos in my_pos)
        opp_mob = sum(len(get_valid_moves(board, pos)) for pos in opp_pos)

        return my_mob - opp_mob
