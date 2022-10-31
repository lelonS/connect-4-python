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

    def is_legal_move():
        pass

    def make_move():
        pass

    def check_win():
        pass
