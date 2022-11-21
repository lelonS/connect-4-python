class ConnectFour:
    board: list[list[int]]  # board[col][row]
    turn: int = 0
    total_cols: int
    total_rows: int
    number_of_players: int = 2  # Max 5

    def __init__(self, total_cols: int, total_rows: int) -> None:
        self.total_cols = total_cols
        self.total_rows = total_rows
        self.board = [[] for _ in range(total_cols)]

    def is_legal_move(self, col: int) -> bool:
        # Check if col is out of bounds and if col is full
        return 0 <= col < self.total_cols and len(self.board[col]) < self.total_rows

    def make_move(self, col: int) -> bool:
        # Check if move is legal
        if self.is_legal_move(col):
            # Append turn to column
            self.board[col].append(self.turn)
            # Change turn 0 -> 1 -> 0
            # self.turn = 1 if self.turn == 0 else 0
            self.turn = (self.turn + 1) % self.number_of_players
            return True  # Move made success
        return False  # Move not made

    def check_win_dir(self, col: int, row: int, direction: tuple[int, int]) -> int:
        """From the col and row a piece is placed, the function takes
        a direction and returns the number of pieces that share the same
        value in a direction (not including the placed piece)."""
        current_plr_pos = self.board[col][row]
        counter = 0

        for i in range(1, 4):
            col_check = col + i * direction[0]
            row_check = row + i * direction[1]
            # Stops looking for pieces if the next one is out of bounds
            if 0 > col_check or col_check >= self.total_cols:
                break
            if 0 > row_check or row_check >= len(self.board[col_check]):
                break
            # Adds to the counter when we find a piece that share the same value
            if current_plr_pos == self.board[col_check][row_check]:
                counter += 1
            else:
                break
        return counter

    def check_win_at(self, col: int, row: int) -> bool:
        # direction_list = [left, left-down, down, right-down] ← ↙ ↓ ↘
        # direction_list_opp = [right, right-up, up, left-up] → ↗ ↑ ↖
        direction_list = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
        direction_list_opp = [(1, 0), (1, 1), (0, 1), (-1, 1)]

        for i in range(4):
            first_check = self.check_win_dir(col, row, direction_list[i])
            second_check = self.check_win_dir(col, row, direction_list_opp[i])

            # return True if there are 4 or more pieces in a row from any direction
            if first_check + second_check + 1 >= 4:
                return True
        return False

    def reset_game(self):
        self.board = [[] for _ in range(self.total_cols)]

    def check_board_full(self) -> bool:
        # Check if any legal move exists
        for col in range(self.total_cols):
            if self.is_legal_move(col):
                return False
        # No legal move exists
        return True
