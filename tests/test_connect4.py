import pytest
from classes.connect4 import ConnectFour

# Full board
test_win_board1 = [
    [1, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 1],
    [2, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1]
]
# Half-empty board (don't fill board)
test_win_board2 = [
    [0, 0, 0],
    [0, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 0, 1],
    [1, 1, 1],
    [0, 1, 1, 1, 0, 1],
    [2, 0, 0, 0, 1, 1],
    [0, 0]
]
LEFT = (-1, 0)  # ←
RIGHT = (1, 0)  # →
UP = (0, -1)  # ↑
DOWN = (0, 1)  # ↓
RIGHT_UP = (1, 1)  # ↗
LEFT_DOWN = (-1, -1)  # ↙
LEFT_UP = (-1, 1)  # ↖
RIGHT_DOWN = (1, -1)  # ↘

test_win_data = [
    (4, 2, True),
    (0, 5, True),
    (3, 2, True),
    (3, 0, True),
    (0, 0, False)
]

test_legal_move_data = [
    (None, 0, True),
    (None, -1, False),
    (None, 7, False),
    (None, 6, True),
    (test_win_board1, 0, False)
]

test_board_full_data = [
    (test_win_board1, True),
    (test_win_board2, False),
    (None, False)
]


@pytest.mark.parametrize("col, row, output", test_win_data)
def test_check_win_at(col, row, output):
    c = ConnectFour(7, 6)
    c.board = test_win_board1
    assert c.check_win_at(col, row) == output


@pytest.mark.parametrize("board, col, output", test_legal_move_data)
def test_is_legal_move(board, col, output):
    c = ConnectFour(7, 6)
    if board is not None:
        c.board = board
    assert c.is_legal_move(col) == output


@pytest.mark.parametrize("board, output", test_board_full_data)
def test_check_board_full(board, output):
    c = ConnectFour(7, 6)
    if board is not None:
        c.board = board
    assert c.check_board_full() == output
