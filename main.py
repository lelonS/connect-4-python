import pygame
from constants import WIDTH, HEIGHT
import drawer
from classes.connect4 import ConnectFour
from drawer import draw_board, get_col_from_x


def main():
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    # Temp create ConnectFour to test draw grid and draw piece
    c = ConnectFour(7, 6)
    game_over = False

    draw_board(screen, c)
    pygame.display.update()

    # Loop
    running = True
    while running:
        screen.fill(drawer.BLACK)
        mouse_pos = pygame.mouse.get_pos()
        mouse_col = get_col_from_x(mouse_pos[0])
        if game_over:
            # Draw win text
            drawer.draw_text(
                screen, "You won!! Press R to restart", 32, 200, 50, (0, 255, 0))
        else:
            # Draw column mouse hovers over
            drawer.hover_mouse(screen, mouse_col, c.total_rows, c.turn)

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                move_success = c.make_move(mouse_col)
                if move_success and c.check_win_at(mouse_col, len(c.board[mouse_col]) - 1):
                    # Someone won
                    game_over = True
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    # Reset game
                    c.reset_game()
                    game_over = False

        draw_board(screen, c)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
