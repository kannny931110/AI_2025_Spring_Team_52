from typing import List, Tuple
from board import Board
from rules import get_valid_moves, get_valid_arrows
import time

class HeuristicAgent:
    def __init__(self, agent_id: int, max_depth: int = 3, time_limit: float = 2.0,
                 weight_mobility: float = 0.4, weight_territory: float = 0.4):
        self.agent_id = agent_id
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.weight_mobility = weight_mobility
        self.weight_territory = weight_territory
        self.start_time = None

    def get_action(self, board: Board) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        self.start_time = time.time()
        pos_list = board.agent_1_pos if self.agent_id == 1 else board.agent_2_pos
        best_score = float('-inf')
        best_action = None

        for from_pos in pos_list:
            for to_pos in get_valid_moves(board, from_pos):
                for arrow_pos in get_valid_arrows(board, to_pos):
                    board_copy = board.clone()
                    try:
                        board_copy.move(from_pos, to_pos, self.agent_id)
                        board_copy.arrow_place(to_pos, arrow_pos, self.agent_id)
                        board_copy.update_temp_blocks()
                    except:
                        continue

                    score = self.alpha_beta(board_copy, depth=self.max_depth - 1, alpha=float('-inf'), beta=float('inf'), maximizing=False)
                    if score > best_score:
                        best_score = score
                        best_action = (from_pos, to_pos, arrow_pos)

                    if time.time() - self.start_time > self.time_limit:
                        break

        if best_action:
            return best_action
        else:
            raise ValueError("No valid moves or arrows available.")

    def alpha_beta(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        if depth == 0 or time.time() - self.start_time > self.time_limit:
            return self.board_eval(board)

        current_agent_id = self.agent_id if maximizing else 3 - self.agent_id
        pos_list = board.agent_1_pos if current_agent_id == 1 else board.agent_2_pos

        if maximizing:
            max_eval = float('-inf')
            for from_pos in pos_list:
                for to_pos in get_valid_moves(board, from_pos):
                    for arrow_pos in get_valid_arrows(board, to_pos):
                        board_copy = board.clone()
                        try:
                            board_copy.move(from_pos, to_pos, current_agent_id)
                            board_copy.arrow_place(to_pos, arrow_pos, current_agent_id)
                            board_copy.update_temp_blocks()
                        except:
                            continue
                        eval = self.alpha_beta(board_copy, depth - 1, alpha, beta, False)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            return max_eval
                        if time.time() - self.start_time > self.time_limit:
                            return max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for from_pos in pos_list:
                for to_pos in get_valid_moves(board, from_pos):
                    for arrow_pos in get_valid_arrows(board, to_pos):
                        board_copy = board.clone()
                        try:
                            board_copy.move(from_pos, to_pos, current_agent_id)
                            board_copy.arrow_place(to_pos, arrow_pos, current_agent_id)
                            board_copy.update_temp_blocks()
                        except:
                            continue
                        eval = self.alpha_beta(board_copy, depth - 1, alpha, beta, True)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            return min_eval
                        if time.time() - self.start_time > self.time_limit:
                            return min_eval
            return min_eval

    def board_eval(self, board: Board) -> float:
        my_pos = board.agent_1_pos if self.agent_id == 1 else board.agent_2_pos
        opp_pos = board.agent_2_pos if self.agent_id == 1 else board.agent_1_pos

        my_mob = sum(len(get_valid_moves(board, pos)) for pos in my_pos)
        opp_mob = sum(len(get_valid_moves(board, pos)) for pos in opp_pos)

        my_terr = self.territory_est(board, my_pos)
        opp_terr = self.territory_est(board, opp_pos)

        center = board.size // 2
        my_centrality = -sum(abs(x - center) + abs(y - center) for x, y in my_pos)

        return self.weight_mobility * (my_mob - opp_mob) + self.weight_territory * (my_terr - opp_terr) + 0.2 * my_centrality

    def territory_est(self, board: Board, pos: List[Tuple[int, int]]) -> int:
        visited = set()
        frontier = list(pos)
        count = 0
        while frontier:
            x, y = frontier.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            count += 1
            for dx, dy in board.DIRECTIONS:
                nx, ny = x + dx, y + dy
                if board.bound_check(nx, ny) and not board.block_stat_check(nx, ny) and (nx, ny) not in visited:
                    frontier.append((nx, ny))
        return count
