class ConnectFour:
    board: list[list[int]]  # board[col][row]
    turn: int = 0
    total_cols: int
    total_rows: int

    def __init__(self, total_cols: int, total_rows: int) -> None:
        self.total_cols = total_cols
        self.total_rows = total_rows
        self.board = [[] for _ in range(total_cols)]

    def is_legal_move(self, col: int) -> bool:
        # Check if col is out of bounds and if row is full
        return col < self.total_cols and len(self.board[col]) < self.total_rows

    def make_move(self, col: int):
        # Check if move is legal
        if self.is_legal_move(col):
            # Append turn to column
            self.board[col].append(self.turn)
            # Change turn 0 -> 1 -> 0
            self.turn = 1 if self.turn == 0 else 0

    def check_win(self):
        pass
