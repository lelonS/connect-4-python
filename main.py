import pygame
from classes.connect4 import ConnectFour

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME = (0, 255, 0)

# Screen parameters
WIDTH = 900
HEIGHT = 600

# Variables
TILE_SIZE = 80


def draw_grid(screen: pygame.Surface, w: int, h: int):
    # Draws grid in bottom left corner

    # Draw rows
    start_x = 0
    end_x = TILE_SIZE * w
    for row in range(0, h + 1):
        y_coord = HEIGHT - row * TILE_SIZE
        pygame.draw.line(screen, WHITE, (start_x, y_coord), (end_x, y_coord))

    # Draw columns
    start_y = HEIGHT
    end_y = HEIGHT - TILE_SIZE * h
    for col in range(0, w + 1):
        x_coord = col * TILE_SIZE
        pygame.draw.line(screen, WHITE, (x_coord, start_y), (x_coord, end_y))


def draw_pieces(screen: pygame.Surface, board: list[list[int]]):
    # Player colors
    colors = [(255, 0, 0), (0, 0, 255), LIME]

    # Variables
    half_tile = TILE_SIZE / 2

    for col_num in range(len(board)):
        # Middle of column
        x_mid = col_num * TILE_SIZE + half_tile
        for row_num in range(len(board[col_num])):
            # Middle of row
            y_mid = HEIGHT - row_num * TILE_SIZE - half_tile
            # Player (non-negative int)
            plr = board[col_num][row_num]

            # Draw piece
            pygame.draw.circle(screen, colors[plr], (x_mid, y_mid), half_tile)


def get_col_from_x(x: int) -> int:
    return x // TILE_SIZE


def main():
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    # Temp create ConnectFour to test draw grid and draw piece
    c = ConnectFour(7, 6)

    # Draw board
    screen.fill(BLACK)
    draw_pieces(screen, c.board)
    draw_grid(screen, c.total_cols, c.total_rows)
    pygame.display.update()

    # Loop
    running = True
    while running:

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                col = get_col_from_x(mouse_pos[0])
                c.make_move(col)

                screen.fill(BLACK)
                draw_pieces(screen, c.board)
                draw_grid(screen, c.total_cols, c.total_rows)
                pygame.display.update()


if __name__ == '__main__':
    main()
