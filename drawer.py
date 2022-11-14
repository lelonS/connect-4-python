import pygame
from classes.connect4 import ConnectFour

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)

# Variables
BOARD_BOTTOM_LEFT = (0, 600)

TILE_SIZE = 80


def get_col_from_x(x: int) -> int:
    return (x - BOARD_BOTTOM_LEFT[0]) // TILE_SIZE


def get_tile_pos(col: int, row: int) -> tuple[float, float]:
    """Returns top left point of tile"""
    # Col
    x_coord = BOARD_BOTTOM_LEFT[0] + col * TILE_SIZE
    # Row
    y_coord = BOARD_BOTTOM_LEFT[1] - (row + 1) * TILE_SIZE
    return x_coord, y_coord


def draw_board_overlay(screen: pygame.Surface, cols: int, rows: int):
    # Draws grid
    surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    # Fill with transparent background
    surf.fill((255, 255, 255, 0))

    for col_num in range(cols):
        for row_num in range(rows):
            x_pos, y_pos = get_tile_pos(col_num, row_num)

            pygame.draw.rect(surf, WHITE,
                             (x_pos, y_pos, TILE_SIZE, TILE_SIZE), width=2)
    screen.blit(surf, (0, 0))


def draw_piece(screen: pygame.Surface, pos: tuple[float, float], plr: int):
    """Variable pos is top left of the rect the circle is inside"""
    # Variables
    half_tile = TILE_SIZE / 2

    # Player colors
    colors = [RED, BLUE]

    x_pos, y_pos = pos

    # Get middle of tile
    x_mid = x_pos + TILE_SIZE / 2
    y_mid = y_pos + TILE_SIZE / 2

    # Draw piece
    pygame.draw.circle(screen, colors[plr], (x_mid, y_mid), half_tile)


def draw_piece_at_col(screen: pygame.Surface, col: int, row: int, plr: int):
    pos = get_tile_pos(col, row)
    draw_piece(screen, pos, plr)


def draw_pieces(screen: pygame.Surface, board: list[list[int]], falling_pieces: dict):
    """Draw all pieces in board"""
    for col_num in range(len(board)):
        for row_num in range(len(board[col_num])):
            # Check if piece animated
            if (col_num, row_num) in falling_pieces:
                piece = falling_pieces[(col_num, row_num)]
                draw_piece(screen, (piece.x, piece.y), board[col_num][row_num])
            else:
                draw_piece_at_col(screen, col_num, row_num,
                                  board[col_num][row_num])


def draw_text(screen: pygame.Surface, text: str, size: int, x: int, y: int, color: tuple):
    font = pygame.font.SysFont("consolas", size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


def hover_mouse(screen: pygame.Surface, col: int, row: int, plr: int):
    draw_piece_at_col(screen, col, row, plr)


def draw_board(screen: pygame.Surface, game: ConnectFour, falling_pieces: dict):
    # Draw board
    draw_pieces(screen, game.board,  falling_pieces)
    draw_board_overlay(screen, game.total_cols, game.total_rows)
