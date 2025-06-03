from typing import List, Tuple
from board import Board

def get_valid_moves(board: Board, from_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        moves = []      # Append all valid moves to this list
        for dx, dy in board.DIRECTIONS:
            x,y= from_pos
            while True:
                x += dx
                y += dy
                if not board.bound_check(x, y) or board.block_stat_check(x, y):
                    break
                moves.append((x, y))
        return moves

def get_valid_arrows(board: Board, arrow_from: Tuple[int, int]) -> List[Tuple[int, int]]:
    return get_valid_moves(board, arrow_from)