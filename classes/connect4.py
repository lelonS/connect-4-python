class ConnectFour:
    board: list[list[int]]  # board[col][row]
    turn: int = 0
    total_cols: int
    total_rows: int

    def __init__(self, total_cols: int, total_rows: int) -> None:
        self.total_cols = total_cols
        self.total_rows = total_rows
        # put "-1" in every empty tile on board.
        self.board = [[-1] * total_rows for _ in range(total_cols)]

    def is_legal_move(self, col: int) -> bool:
        return self.board[col][-1] == -1

    def make_move(self):
        pass

    def check_win(self):
        pass
