import pygame
from classes.connect4 import ConnectFour
from drawer import draw_pieces, draw_board_overlay
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIME = (0, 255, 0)

# Screen parameters
WIDTH = 900
HEIGHT = 600

# Variables
TILE_SIZE = 80


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
    draw_board_overlay(screen, c.total_cols, c.total_rows)

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
                draw_board_overlay(screen, c.total_cols, c.total_rows)
                # draw_grid(screen, c.total_cols, c.total_rows)
                pygame.display.update()


if __name__ == '__main__':
    main()
