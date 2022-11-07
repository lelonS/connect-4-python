import pygame


BOARD_BOTTOM_LEFT = (0, 600)
TILE_SIZE = 80


def get_tile_pos(col: int, row: int) -> tuple[float, float]:
    '''Returns top left point of tile'''
    # Col
    x_coord = col * TILE_SIZE
    # Row
    y_coord = BOARD_BOTTOM_LEFT[1] - (row + 1) * TILE_SIZE
    print(x_coord, y_coord)
    return (x_coord, y_coord)


def draw_board_overlay(screen: pygame.Surface, cols: int, rows: int):
    # Draws grid
    surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    surf.fill((255, 255, 255, 0))

    # pygame.draw.rect(surf, (0, 100, 255, 155), (0, 0, 162, 100), 21)
    for col_num in range(cols):
        for row_num in range(rows):
            x_pos, y_pos = get_tile_pos(col_num, row_num)

            pygame.draw.rect(surf, (255, 255, 255),
                             (x_pos, y_pos, TILE_SIZE, TILE_SIZE), width=10)
    screen.blit(surf, (0, 0))


def draw_pieces(screen: pygame.Surface, board: list[list[int]]):
    # Player colors
    colors = [(255, 0, 0), (0, 0, 255)]

    # Variables
    half_tile = TILE_SIZE / 2

    for col_num in range(len(board)):
        for row_num in range(len(board[col_num])):
            x_pos, y_pos = get_tile_pos(col_num, row_num)

            x_mid = x_pos + TILE_SIZE / 2
            y_mid = y_pos + TILE_SIZE / 2

            # Player (non-negative int)
            plr = board[col_num][row_num]

            # Draw piece
            pygame.draw.circle(screen, colors[plr], (x_mid, y_mid), half_tile)
