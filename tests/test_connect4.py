import pytest

import classes.connect4
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


@pytest.mark.parametrize("col, row, direction, output", test_win_data)
def test_check_win_dir(col, row, direction, output):
    c = ConnectFour(7, 6)
    c.board = test_win_board1
    assert c.check_win_dir(col, row, direction) == output


def test_is_legal_move():
    pass


def check_board_full():
    pass
