from board import Board
from rules import get_valid_moves, get_valid_arrows

def test_board_display():
    print("=== Test: Board Display ===")
    board = Board(size=10)
    board.amazon_place([(0, 0), (0, 9)], agent_id=1)
    board.amazon_place([(9, 0), (9, 9)], agent_id=2)
    board.display()

def test_basic_move_and_arrow():
    print("=== Test: Basic Move and Arrow ===")
    board = Board(size=10)
    board.amazon_place([(0, 0), (0, 9)], agent_id=1)
    board.amazon_place([(9, 0), (9, 9)], agent_id=2)

    if not board.agent_1_pos:
        raise ValueError("Agent 1 has no pieces on the board.")

    from_pos = board.agent_1_pos[0]
    moves = get_valid_moves(board, from_pos)
    to_pos = moves[0]
    arrows = get_valid_arrows(board, to_pos)
    arrow_pos = arrows[0]

    board.move(from_pos, to_pos, agent_id=1)
    board.arrow_place(to_pos, arrow_pos, agent_id=1)
    board.display()

def test_temp_block():
    print("=== Test: Temporary Block Countdown ===")
    board = Board()
    board.amazon_place([(0, 0)], agent_id=1)

    from_pos = (0, 0)
    to_pos = (1, 0)
    board.move(from_pos, to_pos, agent_id=1)

    valid_arrows = get_valid_arrows(board, to_pos)
    if not valid_arrows:
        raise ValueError("No valid arrow positions found.")
    arrow_pos = valid_arrows[0]

    board.arrow_place(to_pos, arrow_pos, agent_id=1)

    board.display()

    for turn in range(5):
        board.update_temp_blocks()
        print(f"\nAfter turn {turn + 1}:")
        board.display()

if __name__ == "__main__":
    test_board_display()
    test_basic_move_and_arrow()
    test_temp_block()