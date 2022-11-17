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
        # Check if col is out of bounds and if row is full
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

    def check_win_dir(self, col: int, row: int, direction: tuple[int, int]) -> bool:
        """From the col and row a piece is placed, check_dir_win takes
        a direction and counts the same pieces in all directions.
        Returns True if there's 4 or more total pieces in a line. """
        current_plr_pos = self.board[col][row]
        first_check = 0
        second_check = 0

        # First check (i.e. to the left)
        for i in range(1, 4):
            col_check = col + i * direction[0]
            row_check = row + i * direction[1]
            # Stops looking for pieces if the next one is out of bounds
            if 0 > col_check or col_check >= self.total_cols:
                break
            if 0 > row_check or row_check >= len(self.board[col_check]):
                break
            if current_plr_pos == self.board[col_check][row_check]:
                # Adds to the counter when we find an identical piece
                first_check += 1
            else:
                break

        # Second check (reversed direction from first check)
        for i in range(1, 4):
            col_check = col - i * direction[0]
            row_check = row - i * direction[1]
            # Stops looking for pieces if the next one is out of bounds
            if 0 > col_check or col_check >= self.total_cols:
                break
            if 0 > row_check or row_check >= len(self.board[col_check]):
                break
            if current_plr_pos == self.board[col_check][row_check]:
                # Adds to the counter when we find an identical piece
                second_check += 1
            else:
                break

        if first_check + second_check >= 3:
            # Only have to check if total is 3 or more because we don't count
            # initial piece.
            return True
        else:
            return False

    def check_win_at(self, col: int, row: int) -> bool:
        # direction_list = [left, left-down, down, right-down] ← ↙ ↓ ↘
        direction_list = [(-1, 0), (-1, -1), (0, -1), (1, -1)]

        for direction in direction_list:
            # check_dir_win checks the above directions and their opposites.
            # That way we check victory condition for all directions.
            if self.check_win_dir(col, row, direction):
                return True
        return False

    def reset_game(self):
        self.board = [[] for _ in range(self.total_cols)]
