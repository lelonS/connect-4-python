import pygame
from classes.falling_point import FallingPoint
from classes.connect4 import ConnectFour
from classes.player import Player
from constants import SEABLUE, BLACK, PLR_COLORS, TILE_SIZE, WHITE
from drawer import draw_text


class GameScene:
    screen: pygame.Surface
    game: ConnectFour
    falling_pieces: dict[tuple, FallingPoint]

    tile_size: int
    board_bottom_left: tuple[int, int]
    players: list[Player]
    player_colors = list[tuple[int, int, int]]

    def __init__(self, screen: pygame.Surface, board_bl: tuple[int, int], cols: int, rows: int, plrs: list[Player]):
        self.screen = screen
        self.falling_pieces = {}
        self.tile_size = TILE_SIZE
        self.board_bottom_left = board_bl
        self.players = plrs
        self.player_colors = PLR_COLORS
        self.game = ConnectFour(cols, rows)

    def get_col_from_x(self, x: int) -> int:
        return (x - self.board_bottom_left[0]) // self.tile_size

    def get_tile_pos(self, col: int, row: int) -> tuple[float, float]:
        """Returns top left point of tile"""
        # Col
        x_coord = self.board_bottom_left[0] + col * self.tile_size
        # Row
        y_coord = self.board_bottom_left[1] - (row + 1) * self.tile_size
        return x_coord, y_coord

    def draw_board_overlay(self, cols: int, rows: int):
        """Draws the board overlay with circle cutouts"""
        # Create surface to use for each tile
        tile_surface = pygame.Surface(
            (self.tile_size, self.tile_size), pygame.SRCALPHA)
        # Fill with blue background
        tile_surface.fill(SEABLUE)
        # Draw circle cutout
        pygame.draw.circle(tile_surface, (0, 0, 0, 0),
                           (self.tile_size / 2, self.tile_size / 2), self.tile_size * 0.45)

        for col_num in range(cols):
            for row_num in range(rows):
                # Draw tile_surface to screen at each tile
                pos = self.get_tile_pos(col_num, row_num)
                self.screen.blit(tile_surface, pos)

    def draw_piece(self, pos: tuple[float, float], plr: int):
        """Variable pos is top left of the rect the circle is inside"""
        # Variables
        half_tile = self.tile_size / 2

        x_pos, y_pos = pos

        # Get middle of tile
        x_mid = x_pos + half_tile
        y_mid = y_pos + half_tile

        plr_color = self.player_colors[plr]  # self.players[plr].color
        # Draw piece
        pygame.draw.circle(
            self.screen, plr_color, (x_mid, y_mid), half_tile)

    def draw_piece_at_tile(self, col: int, row: int, plr: int):
        pos = self.get_tile_pos(col, row)
        self.draw_piece(pos, plr)

    def draw_pieces(self):
        """Draw all pieces in board"""
        board = self.game.board
        for col_num in range(len(board)):
            for row_num in range(len(board[col_num])):
                # Check if piece animated
                if (col_num, row_num) in self.falling_pieces:
                    piece = self.falling_pieces[(col_num, row_num)]
                    self.draw_piece((piece.x, piece.y),
                                    board[col_num][row_num])
                else:
                    self.draw_piece_at_tile(col_num, row_num,
                                            board[col_num][row_num])

    def update_all_falling(self, dt: float):
        """Updates all falling pieces"""
        # Pieces past max_y to remove
        keys_to_remove = []

        # Update all falling pieces
        for key in self.falling_pieces:
            self.falling_pieces[key].update(dt)
            if self.falling_pieces[key].is_past_max:
                keys_to_remove.append(key)

        # Remove pieces past max_y
        for key in keys_to_remove:
            del self.falling_pieces[key]

    def check_all_past(self, past_y: float) -> bool:
        """Checks if all falling pieces are past a certain y value"""
        for piece in self.falling_pieces.values():
            if piece.y <= past_y:
                return False
        return True

    def handle_event(self, event: pygame.event.Event, mouse_col: int, can_move: bool):
        """Checks event type and handles it"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and can_move:
            move_success = self.game.make_move(mouse_col)
            if move_success:
                landed_row = len(self.game.board[mouse_col]) - 1
                top_pos = self.get_tile_pos(
                    mouse_col, self.game.total_rows)
                landed_pos = self.get_tile_pos(mouse_col, landed_row)

                # Create animated piece and add to dictionary
                self.falling_pieces[(mouse_col, landed_row)] = FallingPoint(
                    top_pos, 0, 2300, landed_pos[1])

        elif event.type == pygame.KEYDOWN:
            if self.game.is_won or self.game.is_tied and event.key == pygame.K_r:
                # Reset game
                self.game.reset_game()

    def draw_win_line(self):

        # Check if all pieces has fallen
        if len(self.falling_pieces) > 0:
            return

        # All pieces have fallen
        # Get winning line tiles
        col_1, row_1 = self.game.winner_tile_1
        col_2, row_2 = self.game.winner_tile_2
        # Get positions of tiles
        x_1, y_1 = self.get_tile_pos(col_1, row_1)
        x_2, y_2 = self.get_tile_pos(col_2, row_2)
        # Get middle of tiles
        h_tile = self.tile_size / 2
        pos_1 = (x_1 + h_tile, y_1 + h_tile)
        pos_2 = (x_2 + h_tile, y_2 + h_tile)
        pygame.draw.line(self.screen, WHITE, pos_1, pos_2, width=10)

    def draw_result_info(self):
        if self.game.is_won:
            # Draw win text
            draw_text(self.screen, f"Player {self.game.winner + 1} won!! [R]estart, [M]enu", 32, 200, 50,
                      self.player_colors[self.game.winner])
            # Draw win line
            self.draw_win_line()

        elif self.game.is_tied:
            # Draw tie text
            draw_text(self.screen, "Tie... [R]estart, [M]enu",
                      32, 200, 50, (125, 125, 125))

    def run_game(self):

        # Create caption
        pygame.display.set_caption("Connect4")

        # Dictionary (col, row):FallingPoint
        clock = pygame.time.Clock()

        # Loop
        running = True
        while running:
            self.screen.fill(BLACK)

            # Get clock info
            ms = clock.tick()
            seconds = ms / 1000
            self.update_all_falling(seconds)

            # Get mouse info
            mouse_pos = pygame.mouse.get_pos()
            mouse_col = self.get_col_from_x(mouse_pos[0])

            # Check if all falling pieces past or in top row
            all_past = self.check_all_past(
                self.get_tile_pos(0, self.game.total_rows - 1)[1])
            can_move = all_past and not self.game.is_won and not self.game.is_tied

            # Drawing
            if can_move:
                # Draw column mouse hovers over if user can move
                self.draw_piece_at_tile(
                    mouse_col, self.game.total_rows, self.game.turn)

            self.draw_pieces()
            self.draw_board_overlay(self.game.total_cols, self.game.total_rows)
            self.draw_result_info()
            pygame.display.update()

            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    # Go to menu
                    running = False
                else:
                    self.handle_event(event, mouse_col, can_move)


if __name__ == "__main__":
    pygame.init()
    s = pygame.display.set_mode((900, 600))
    game_screen = GameScene(s, (0, 600), 7, 6, [Player("name", (255, 0, 0))])
    game_screen.run_game()
