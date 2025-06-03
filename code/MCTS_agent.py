import random
import copy
import math
import time
from typing import List, Tuple, Optional
from board import Board
from rules import get_valid_moves, get_valid_arrows

class MCTSNode:
    def __init__(self, board: Board, agent_id: int, parent=None):
        self.board = board
        self.agent_id = agent_id
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.untried_actions = self.get_all_actions()

    def get_all_actions(self) -> List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
        positions = self.board.agent_1_pos if self.agent_id == 1 else self.board.agent_2_pos
        actions = []
        for from_pos in positions:
            for to_pos in get_valid_moves(self.board, from_pos):
                for arrow_pos in get_valid_arrows(self.board, to_pos):
                    actions.append((from_pos, to_pos, arrow_pos))
        return actions

    def expand(self):
        action = self.untried_actions.pop()
        board_copy = copy.deepcopy(self.board)
        board_copy.move(action[0], action[1], self.agent_id)
        board_copy.arrow_place(action[1], action[2], self.agent_id)
        board_copy.update_temp_blocks()
        next_player = 3 - self.agent_id
        child_node = MCTSNode(board_copy, next_player, parent=self)
        self.children.append((child_node, action))
        return child_node

    def best_child(self, c_param: float = 1.41) -> "MCTSNode":
        best_score = float('-inf')
        best_node: Optional["MCTSNode"] = None

        for child_node, _ in self.children:
            child_node: MCTSNode = child_node
            if child_node.visits == 0:
                continue
            exploit = child_node.value / child_node.visits
            explore = math.sqrt(2 * math.log(self.visits) / child_node.visits)
            ucb1 = exploit + c_param * explore

            if ucb1 > best_score:
                best_score = ucb1
                best_node = child_node

        if best_node is None:
            raise ValueError("No valid child found in best_child().")

        return best_node

    def backpropagate(self, result: int):
        self.visits += 1
        if self.agent_id == result:
            self.value += 1
        elif result == 0:
            self.value += 0.5
        if self.parent:
            parent: MCTSNode = self.parent
            parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def is_terminal_node(self):
        return not self.get_all_actions()


class MCTSAgent:
    def __init__(self, agent_id: int, time_limit: float = 2.0):
        self.agent_id = agent_id
        self.time_limit = time_limit

    def get_action(self, board: Board) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        root = MCTSNode(copy.deepcopy(board), self.agent_id)
        start = time.time()

        while time.time() - start < self.time_limit:
            node = root
            while not node.is_terminal_node() and node.is_fully_expanded():
                node = node.best_child()
            if not node.is_terminal_node() and node.untried_actions:
                node = node.expand()
            result = self.simulate(node.board)
            node.backpropagate(result)

        if root.children:
            best_child = root.best_child(c_param=0)
            for child, action in root.children:
                if child == best_child:
                    return action

        return self.fallback_action(board)

    def simulate(self, board: Board) -> int:
        my_pos = board.agent_1_pos if self.agent_id == 1 else board.agent_2_pos
        opp_pos = board.agent_2_pos if self.agent_id == 1 else board.agent_1_pos

        my_mob = sum(len(get_valid_moves(board, pos)) for pos in my_pos)
        opp_mob = sum(len(get_valid_moves(board, pos)) for pos in opp_pos)

        my_terr = self.territory_est(board, my_pos)
        opp_terr = self.territory_est(board, opp_pos)

        score = (my_mob - opp_mob) + 0.5 * (my_terr - opp_terr)
        if score > 0:
            return self.agent_id
        elif score < 0:
            return 3 - self.agent_id
        return 0

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

    def fallback_action(self, board: Board):
        pos = board.agent_1_pos if self.agent_id == 1 else board.agent_2_pos
        legal = []
        for from_pos in pos:
            for to_pos in get_valid_moves(board, from_pos):
                for arrow in get_valid_arrows(board, to_pos):
                    legal.append((from_pos, to_pos, arrow))
        if not legal:
            raise ValueError("No valid fallback action")
        return random.choice(legal)
