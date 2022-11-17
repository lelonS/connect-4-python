import pytest
from classes.connect4 import ConnectFour


test_win_board1 = [
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1],
]
LEFT = (-1, 0)
LEFT_DOWN = (-1, -1)
DOWN = (0, -1)
RIGHT_DOWN = (1, -1)

test_win_data = [
    (3, 5, LEFT, True)
]

test_legal_move_data = [
    (None, 0, True),
    (None, -1, False),
    (None, 7, False),
    (None, 6, True),
    (test_win_board1, 0, False)
]


@pytest.mark.parametrize("col, row, direction, output", test_win_data)
def test_check_win_dir(col, row, direction, output):
    c = ConnectFour(7, 6)
    c.board = test_win_board1
    assert c.check_win_dir(col, row, direction) == output


@pytest.mark.parametrize("board, col, output", test_legal_move_data)
def test_is_legal_move(board, col, output):
    c = ConnectFour(7, 6)
    if board is not None:
        c.board = board
    assert c.is_legal_move(col) == output


def check_board_full():
    pass
