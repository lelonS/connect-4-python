import pygame

import drawer
from classes.connect4 import ConnectFour
from drawer import draw_board, get_col_from_x

# Screen parameters
WIDTH = 900
HEIGHT = 600


def main():
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    # Temp create ConnectFour to test draw grid and draw piece
    c = ConnectFour(7, 6)

    draw_board(screen, c)

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
                move_success = c.make_move(col)
                draw_board(screen, c)
                if move_success and c.check_win_at(col, len(c.board[col]) - 1):
                    drawer.draw_text(screen, "You won!!", 20, 200, 50)


if __name__ == '__main__':
    main()
