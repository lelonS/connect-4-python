import pygame
from classes.falling_point import FallingPoint
from classes.connect4 import ConnectFour
from classes.player import Player
from constants import SEABLUE, BLACK, PLR_COLORS, TILE_SIZE, WHITE, BOARD_BOTTOM_LEFT, MAX_BOARD_HEIGHT, MAX_BOARD_WIDTH
from constants import HEIGHT
from drawer import draw_text
from classes.scene import Scene, SceneManager


class GameScene(Scene):
    game: ConnectFour
    falling_pieces: dict[tuple, FallingPoint]

    tile_size: int
    board_bottom_left: tuple[int, int]
    players: list[Player]
    player_colors = list[tuple[int, int, int]]

    can_move: bool
    current_hover_col: int

    coin_frame: pygame.Surface
    game_over: bool

    def __init__(self, screen: pygame.Surface, board_bl: tuple[int, int], cols: int, rows: int, plrs: list[Player]):
        super().__init__(screen)
        self.falling_pieces = {}
        self.tile_size = TILE_SIZE
        self.board_bottom_left = board_bl
        self.players = plrs
        self.player_colors = PLR_COLORS
        self.game = ConnectFour(cols, rows, total_players=len(plrs))
        self.game_over = False

        self.can_move = False
        self.current_hover_col = -1
        self.different_boards(cols, rows)
        self.coin_frame = pygame.image.load("assets/coin_frame_fix3.png").convert_alpha()
        self.coin_frame = pygame.transform.smoothscale(self.coin_frame, (self.tile_size, self.tile_size))

    def different_boards(self, cols: int, rows: int):
        max_tile_width = MAX_BOARD_WIDTH // cols
        max_tile_height = MAX_BOARD_HEIGHT // (rows + 1)

        self.tile_size = min(max_tile_width, max_tile_height)

    def get_col_from_x(self, x: int) -> int:
        return (x - self.board_bottom_left[0]) // self.tile_size

    def get_tile_pos(self, col: int, row: int) -> tuple[float, float]:
        """Get the top left position of a tile

        Args:
            col (int): Column number
            row (int): Row number

        Returns:
            tuple[float, float]: Top left position of tile
        """
        # Col
        x_coord = self.board_bottom_left[0] + col * self.tile_size
        # Row
        y_coord = self.board_bottom_left[1] - (row + 1) * self.tile_size
        return x_coord, y_coord

    def draw_board_overlay(self, cols: int, rows: int):
        """Draw the board overlay

        Args:
            cols (int): All columns
            rows (int): All rows
        """
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
        """Draw a piece at a position

        Args:
            pos (tuple[float, float]): Top left position of piece rect
            plr (int): Player index
        """
        # Variables
        half_tile = self.tile_size / 2

        x_pos, y_pos = pos

        # Get middle of tile
        x_mid = x_pos + half_tile
        y_mid = y_pos + half_tile

        plr_color = self.players[plr].color  # self.players[plr].color
        # Draw piece
        pygame.draw.circle(
            self.screen, plr_color, (x_mid, y_mid), half_tile)
        self.screen.blit(self.coin_frame, (x_pos, y_pos))

    def draw_piece_at_tile(self, col: int, row: int, plr: int):
        pos = self.get_tile_pos(col, row)
        self.draw_piece(pos, plr)

    def draw_pieces(self):
        """Draws all pieces in the game board, including falling pieces"""
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
        """Updates all falling pieces

        Args:
            dt (float): Seconds since last update
        """
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
        """Checks if all falling pieces are past a certain y value

        Args:
            past_y (float): The y value all pieces must be past

        Returns:
            bool: all_past
        """
        for piece in self.falling_pieces.values():
            if piece.y <= past_y:
                return False
        return True

    def on_game_over(self):
        """Called ONCE when game is over
        """
        if self.game_over:
            return
        self.game_over = True
        # Add scores to players
        for plr_num, plr in enumerate(self.players):
            plr.games += 1
            if self.game.is_tied:
                plr.ties += 1
            if self.game.winner == plr_num:
                plr.wins += 1

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
        pygame.draw.line(self.screen, WHITE, pos_1, pos_2, width=int(self.tile_size / 10))

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

    def draw_player_names(self):
        dif = 0
        start_x = self.tile_size * self.game.total_cols + 20
        start_y = HEIGHT - len(self.players) * 40
        for plr in self.players:
            text = f"{plr.name}: {plr.wins}"
            draw_text(self.screen, text, 32, start_x, start_y+dif,
                      plr.color)
            dif = dif + 36

    def draw(self):
        self.screen.fill(BLACK)
        if self.can_move:
            # Draw column mouse hovers over if user can move
            self.draw_piece_at_tile(
                self.current_hover_col, self.game.total_rows, self.game.turn)
        self.draw_player_names()
        self.draw_pieces()
        self.draw_board_overlay(self.game.total_cols, self.game.total_rows)
        self.draw_result_info()
        pygame.display.update()

    def update(self, events: list[pygame.event.Event], dt: float, scene_manager: SceneManager):
        # Get clock info
        self.update_all_falling(dt)

        # Get mouse info
        mouse_pos = pygame.mouse.get_pos()
        mouse_col = self.get_col_from_x(mouse_pos[0])

        # Check if all falling pieces past or in top row
        all_past = self.check_all_past(
            self.get_tile_pos(0, self.game.total_rows - 1)[1])
        self.can_move = all_past and not self.game.is_won and not self.game.is_tied

        # Handle pygame events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.can_move:
                # Attempt move
                move_success = self.game.make_move(mouse_col)
                if move_success:
                    # Get move info
                    landed_row = len(self.game.board[mouse_col]) - 1
                    landed_pos = self.get_tile_pos(mouse_col, landed_row)
                    top_pos = self.get_tile_pos(
                        mouse_col, self.game.total_rows)
                    # Create animated piece and add to dictionary
                    self.falling_pieces[(mouse_col, landed_row)] = FallingPoint(
                        top_pos, 0, 2300, landed_pos[1])

            elif event.type == pygame.KEYDOWN:
                if (self.game.is_won or self.game.is_tied) and event.key == pygame.K_r:
                    # Reset game
                    self.game.reset_game()
                    self.game_over = False
                elif event.key == pygame.K_m:
                    # Go to menu
                    scene_manager.go_to_origin_scene()

        if self.game.is_won or self.game.is_tied and not self.game_over:
            self.on_game_over()
        self.current_hover_col = mouse_col


if __name__ == "__main__":
    pygame.init()
    s = pygame.display.set_mode((900, 600))
    clock = pygame.time.Clock()
    sceneManager = SceneManager()
    sceneManager.add_scene(GameScene(s, BOARD_BOTTOM_LEFT, 7, 6, [
        Player("test", (255, 0, 0))]))
    while True:
        seconds = clock.tick() / 1000
        evs = pygame.event.get()
        for e in evs:
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
        sceneManager.update(evs, seconds)
        sceneManager.draw()