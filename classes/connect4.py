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
            # self.turn = 1 if self.turn == 0 else 0
            self.turn = (self.turn + 1) % 2
            print(self.check_win_at(col, len(self.board[col]) - 1))

    def check_direction_win(self, col: int, row: int, direction: tuple[int, int]) -> bool:  # Check horizontal win
        current_plr_pos = self.board[col][row]
        first_check = 0
        second_check = 0

        for i in range(1, 4):
            col_check = col + i * direction[0]
            row_check = row + i * direction[1]
            if 0 > col_check or col_check >= self.total_cols:
                break
            if 0 > row_check or row_check >= len(self.board[col_check]):
                break
            if current_plr_pos == self.board[col_check][row_check]:
                first_check += 1
            else:
                break

        for i in range(1, 4):
            col_check = col - i * direction[0]
            row_check = row - i * direction[1]
            if 0 > col_check or col_check >= self.total_cols:
                break
            if 0 > row_check or row_check >= len(self.board[col_check]):
                break
            if current_plr_pos == self.board[col_check][row_check]:
                second_check += 1
            else:
                break

        if first_check + second_check >= 3:
            return True

    def check_win_at(self, col: int, row: int) -> bool:

        direction_list = [(-1, 0), (-1, -1), (0, -1), (1, -1)]  # left, left-bottom, bottom, right-bottom

        for direction in direction_list:
            if self.check_direction_win(col, row, direction):
                return True
        return False

        # if current_plr_pos == self.board[col - 1][row]:  # check 1 step to the left
        #     if current_plr_pos == self.board[col - 2][row]:  # check 2 steps to the left
        #         if current_plr_pos == self.board[col - 3][row]:  # check 3 steps to the left
        #             return True  # 4 in a row (3 left of current)
        #         elif current_plr_pos == self.board[col + 1][row]:  # check 2 steps to the left and 1 to the right
        #             return True  # 4 in a row (2 left and 1 right of current)
        #     elif current_plr_pos == self.board[col + 1][row]:  # check 1 step to the left and 1 step to the right
        #         if current_plr_pos == self.board[col + 2][row]:  # check 1 step to the left and 2 steps to the right
        #             return True  # 4 in a row (1 left and 2 right of current)
        # elif current_plr_pos == self.board[col + 1][row]:  # check 1 step to the right
        #     if current_plr_pos == self.board[col + 2][row]:  # check 2 steps to the right
        #         if current_plr_pos == self.board[col + 3][row]:  # check 3 steps to the right
        #             return True  # 4 in a row (3 right of current)
        #         elif current_plr_pos == self.board[col - 1][row]:  # check 2 steps to the right and 1 to the left
        #             return True  # 4 in a row (2 right and 1 left of current)
        #     elif current_plr_pos == self.board[col - 1][row]:  # check 1 step to the right and 1 step to the left
        #         if current_plr_pos == self.board[col - 2][row]:  # check 1 step to the right and 2 steps to the left
        #             return True  # 4 in a row (1 right and 2 left of current)
        #     else:
        #         return False

    def reset_game(self):
        self.board = [[] for _ in range(self.total_cols)]



