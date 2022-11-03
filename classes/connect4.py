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
        return len(self.board[col]) < self.total_rows and col < self.total_cols

    def make_move(self, col: int):
        # Check if move is legal

        # Append turn to column

        # Change turn 0 -> 1 -> 0
        pass

    def check_win(self):
        pass
