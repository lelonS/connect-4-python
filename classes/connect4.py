class ConnectFour:
    board: list[list[int]]  # board[col][row]
    turn: int = 0

    def __init__(self, size_x, size_y) -> None:
        pass

    def is_legal_move(self, col: int) -> bool:
        return self.board[col][-1] == -1

    def make_move(self):
        pass

    def check_win(self):
        pass
