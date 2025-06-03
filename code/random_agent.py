from typing import Tuple
from board import Board
from rules import get_valid_moves, get_valid_arrows
import random

class RandomAgent:
    def __init__(self, agent_id: int):
        self.agent_id = agent_id

    def get_action(self, board: Board) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        pos_list = board.agent_1_pos if self.agent_id == 1 else board.agent_2_pos
        from_pos = random.choice(pos_list)
        to_pos = random.choice(get_valid_moves(board, from_pos))
        arrow_pos = random.choice(get_valid_arrows(board, to_pos))
        return (from_pos, to_pos, arrow_pos)
