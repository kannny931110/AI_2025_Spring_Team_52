from typing import List, Dict, Tuple, Optional

class tile_stat:
    EMPTY=0
    OCCUPIED=1
    TEMP_BLOCK=2
    BLOCK=3

class Board:
    # Direction config
    DIRECTIONS=[
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, -1), # Up-Left
        (-1, 1),  # Up-Right
        (1, -1),  # Down-Left
        (1, 1)    # Down-Right
    ]

    def __init__(self, size: int=10):
        self.size = size
        # Configure the grid with empty tiles
        # Grid structure: self.grid[row][col]
        self.grid = [[tile_stat.EMPTY for _ in range(size)] for _ in range(size)]
        self.temp_blocks: Dict[Tuple[int, int], int]={}
        self.agent_1_pos=[]
        self.agent_2_pos=[]

    def bound_check(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size
    
    def block_stat_check(self, x: int, y: int) -> bool:
        # Bound check
        if not self.bound_check(x, y):
            return True
        stat= self.grid[x][y]
        # Check if the tile is empty.
        # If not, return True (blocked).
        return stat in (tile_stat.OCCUPIED, tile_stat.TEMP_BLOCK, tile_stat.BLOCK)
    
    def amazon_place(self, positions: List[Tuple[int, int]], agent_id: int):
        for x, y in positions:
            self.grid[x][y] = tile_stat.OCCUPIED    # Place an amazon on the grid
            if agent_id == 1:
                self.agent_1_pos.append((x, y))
            else:
                self.agent_2_pos.append((x, y))
    
    def move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], agent_id: int):
        fx, fy = from_pos
        tx, ty = to_pos
        # Check if the source position is occupied and the destination is valid
        if self.grid[fx][fy] != tile_stat.OCCUPIED:
            raise ValueError("Cannot move from an unoccupied position.")
        if self.block_stat_check(tx, ty):
            raise ValueError("Destination is blocked or out of bounds.")
        # Check if the path is valid
        if not self.valid_path(fx, fy, tx, ty):
            raise ValueError("Invalid path from source to destination.")

        self.grid[fx][fy] = tile_stat.TEMP_BLOCK
        self.temp_blocks[(fx, fy)] = 5 # Temporary block for 5 turns
        self.grid[tx][ty] = tile_stat.OCCUPIED

        # Update the agent's position list
        pos_list = self.agent_1_pos if agent_id == 1 else self.agent_2_pos
        if (fx, fy) in pos_list:
            pos_list.remove((fx, fy))
        pos_list.append((tx, ty))

    def arrow_place(self, arrow_from: Tuple[int, int], arrow_to: Tuple[int, int], agent_id: int):
        fx, fy = arrow_from
        tx, ty = arrow_to
        # Check if the destination is valid
        if self.block_stat_check(tx, ty):
            raise ValueError("Arrow target is blocked or out of bounds.")
        # Check if the path is valid
        if not self.valid_path(fx, fy, tx, ty):
            raise ValueError("Invalid path for arrow placement.")
        
        self.grid[tx][ty] = tile_stat.BLOCK

    def valid_path(self, fx: int, fy: int, tx: int, ty: int) -> bool:
        dx = tx - fx
        dy = ty - fy
        step_x=0 if dx == 0 else (1 if dx > 0 else -1)
        step_y=0 if dy == 0 else (1 if dy > 0 else -1)
        # Check if the move is diagonal, horizontal, or vertical
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False
        x,y=fx+step_x, fy+step_y
        while (x, y) != (tx, ty):
            # Check if the current tile is blocked
            if self.block_stat_check(x, y):
                return False
            x += step_x
            y += step_y
        return not self.block_stat_check(tx, ty)    # Ensure the target is not blocked

    def update_temp_blocks(self):
        to_remove=[]    # Grids that need to be turned to empty
        for (x,y) in self.temp_blocks:
            self.temp_blocks[(x,y)] -= 1
            if self.temp_blocks[(x,y)] <= 0:    # Countdown reached zero
                to_remove.append((x,y))
        for pos in to_remove:
            self.grid[pos[0]][pos[1]] = tile_stat.EMPTY
            del self.temp_blocks[pos]

    def clone(self) -> "Board":
        new_board = Board(self.size)
        new_board.grid = [row[:] for row in self.grid]
        new_board.agent_1_pos = self.agent_1_pos[:]
        new_board.agent_2_pos = self.agent_2_pos[:]
        new_board.temp_blocks = dict(self.temp_blocks)
        return new_board

    
    def display(self, with_coords: bool = False):
        if with_coords:
            from utils import print_board
            print_board(self)
        else:
            symbols={
                tile_stat.EMPTY: 'O',
                tile_stat.OCCUPIED: '●',
                tile_stat.TEMP_BLOCK: '△',
                tile_stat.BLOCK: 'X'
            }
            for row in self.grid:
                print(" ".join(symbols[cell] for cell in row))
            print()