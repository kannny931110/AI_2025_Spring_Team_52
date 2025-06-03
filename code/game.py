from board import Board
from typing import Tuple
import random

class Game:
    def __init__(self, agent_1, agent_2, size: int = 10):
        self.board = Board(size)
        self.agent_1 = agent_1
        self.agent_2 = agent_2
        self.current_turn = 1
        self.init_positions()
    
    def init_positions(self):
        self.sym_pos_gen(self.board, 4)  
    
    def sym_pos_gen(self, board: Board, num_per_agent: int):
        margin = max(1, board.size // 10)
        used= set()
        placed_agent_1 = []
        placed_agent_2 = []

        while len(placed_agent_1) < num_per_agent:
            candidate = []
            for x in range(board.size):
                for y in range(board.size):
                    if x < margin or x >= board.size - margin or y < margin or y >= board.size - margin:
                        if(x,y) in used or board.block_stat_check(x, y):
                            continue
                        # Check for symmetric position
                        opponent_x = board.size - 1 - x
                        opponent_y = board.size - 1 - y
                        if (opponent_x, opponent_y) in used or board.block_stat_check(opponent_x, opponent_y):
                            continue
                        candidate.append((x, y, opponent_x, opponent_y))
            if not candidate:
                raise ValueError("No more symmetric edge positions available.")
            x, y, opponent_x, opponent_y = random.choice(candidate)
            board.amazon_place([(x, y)], agent_id=1)
            board.amazon_place([(opponent_x, opponent_y)], agent_id=2)
            used.add((x, y))
            used.add((opponent_x, opponent_y))
            placed_agent_1.append((x, y))
            placed_agent_2.append((opponent_x, opponent_y))

    def run(self, verbose: bool = True, return_winner: bool = False) -> int:
        while True:
            if verbose:
                print(f"Turn: Player {self.current_turn}")
                self.board.display()

            agent = self.agent_1 if self.current_turn == 1 else self.agent_2
            try:
                from_pos, to_pos, arrow_pos = agent.get_action(self.board)
                self.board.move(from_pos, to_pos, self.current_turn)
                self.board.arrow_place(from_pos, arrow_pos, self.current_turn)
                self.board.update_temp_blocks()
            except ValueError:
                winner = 3 - self.current_turn
                if verbose:
                    print(f"Player {self.current_turn} has no legal moves. Player {winner} wins!")
                return winner if return_winner else None

            self.current_turn = 3 - self.current_turn