class ConnectFour:
    board: list[list[int]]  # board[col][row]
    turn: int = 0
    amount_cols: int
    amount_rows: int

    def __init__(self, amount_cols: int, amount_rows: int) -> None:
        self.amount_cols = amount_cols
        self.amount_rows = amount_rows
        self.board = []
        for _ in range(amount_cols):
            col = []
            for _ in range(amount_rows):
                col.append(-1)  # Empty tile represented with -1
            self.board.append(col)

    def is_legal_move(self, col: int) -> bool:
        return self.board[col][-1] == -1

    def make_move(self):
        pass

    def check_win(self):
        pass
