class ConnectFour:
    """Represent a game of Connect Four

    Attributes:
        board (list[list[int]]): The board, to get a tile use board[col][row]
        turn (int): The current turn, begins at 0
        total_cols (int): The total number of columns
        total_rows (int): The total number of rows
        is_won (bool): True if the game is won, False if not
        is_tied (bool): True if the game is tied, False if not
        winner (int): The player who won the game, -1 if no one has won
        winner_tile_1 (tuple[int, int]): The position of the first tile in a row
        winner_tile_2 (tuple[int, int]): The position of the last tile in a row
    """
    board: list[list[int]]  # board[col][row]
    turn: int = 0
    total_cols: int
    total_rows: int
    number_of_players: int = 2  # Max 4
    is_won: bool = False
    is_tied: bool = False
    winner: int = -1
    winner_tile_1: tuple[int, int]
    winner_tile_2: tuple[int, int]

    def __init__(self, total_cols: int, total_rows: int) -> None:
        self.total_cols = total_cols
        self.total_rows = total_rows
        self.board = [[] for _ in range(total_cols)]

    def is_legal_move(self, col: int) -> bool:
        """Checks if move is possible

        Args:
            col (int): The column to check

        Returns:
            bool: True if move is possible, False if not
        """
        # Check if col is out of bounds and if col is full
        return 0 <= col < self.total_cols and len(self.board[col]) < self.total_rows

    def make_move(self, col: int) -> bool:
        """Attempts to make a move at col and checks if the game is won or tied.

        Args:
            col (int): The column to make a move at

        Returns:
            bool: True if move was made, False if not
        """
        # Check if move is legal
        if self.is_legal_move(col):
            # Append turn to column
            self.board[col].append(self.turn)

            # Check if move won the game
            if self.check_win_at(col, len(self.board[col]) - 1):
                self.is_won = True
                self.winner = self.turn
            elif self.check_board_full():
                self.is_tied = True

            # Change turn 0 -> 1 -> 0
            # self.turn = 1 if self.turn == 0 else 0
            self.turn = (self.turn + 1) % self.number_of_players
            return True  # Move made success
        return False  # Move not made

    def check_win_dir(self, col: int, row: int, direction: tuple[int, int]) -> tuple[int, tuple[int, int]]:
        """Checks how many pieces are in a row in a direction from a piece at col and row.

        Args:
            col (int): Origin column
            row (int): Origin row
            direction (tuple[int, int]): Direction to check (x increase per step, y increase per step)

        Returns:
            tuple[int, tuple[int, int]]: Returns the number of pieces in a row (excluding the origin piece)
             and the position of the last piece in a row
        """
        current_plr_pos = self.board[col][row]
        counter = 0
        furthest_tile = (col, row)
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
                furthest_tile = (col_check, row_check)
            else:
                break
        return counter, furthest_tile

    def check_win_at(self, col: int, row: int) -> bool:
        """Checks if the piece at col and row has won the game.

        Args:
            col (int): Origin column
            row (int): Origin row

        Returns:
            bool: True if the piece at col and row has won the game, False if not
        """
        direction_list = [(-1, 0), (-1, -1), (0, -1), (1, -1)]  # ← ↙ ↓ ↘
        direction_list_opp = [(1, 0), (1, 1), (0, 1), (-1, 1)]  # → ↗ ↑ ↖

        for i in range(4):
            first_check, tile_1 = self.check_win_dir(
                col, row, direction_list[i])
            second_check, tile_2 = self.check_win_dir(
                col, row, direction_list_opp[i])

            # return True if there are 4 or more pieces in a row from any direction
            if first_check + second_check + 1 >= 4:
                self.winner_tile_1 = tile_1
                self.winner_tile_2 = tile_2
                return True
        return False

    def reset_game(self):
        self.board = [[] for _ in range(self.total_cols)]
        self.is_won = False
        self.is_tied = False
        self.winner = -1

    def check_board_full(self) -> bool:
        """Checks if the board is full.

        Returns:
            bool: True if the board is full, False if not
        """
        # Check if any legal move exists
        for col in range(self.total_cols):
            if self.is_legal_move(col):
                return False
        # No legal move exists
        return True
