import pytest
import classes.connect4

test_win_board = [
    [0, 0, 0],
    [0],
    [],
    [0],
    [1],
    [],
    [],
]

test_win_data = [
    (),
    (),
    (),
    (),
]


@pytest.mark.parametrize("col, row, output", test_win_data)
def test_check_win_at(col, row, output):
    assert classes.connect4.ConnectFour.check_win_at(col, row) == output


def test_is_legal_move():
    pass


def check_board_full():
    pass
