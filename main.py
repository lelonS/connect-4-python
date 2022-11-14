import pygame
from classes.falling_point import FallingPoint
from classes.connect4 import ConnectFour
from drawer import draw_board, get_col_from_x, BLACK, draw_text, get_tile_pos, hover_mouse

# Screen parameters
WIDTH = 900
HEIGHT = 600


def update_all_falling(falling_pieces: dict, dt: float):
    keys_to_remove = []
    for key in falling_pieces:
        falling_pieces[key].update(dt)
        if falling_pieces[key].is_past_max:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del falling_pieces[key]


def main():
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    # Temp create ConnectFour to test draw grid and draw piece
    c = ConnectFour(7, 6)
    game_over = False

    # Dictionary (col, row):FallingPoint
    falling_pieces = {}
    clock = pygame.time.Clock()

    draw_board(screen, c, falling_pieces)
    pygame.display.update()

    # Loop
    running = True
    while running:
        screen.fill(BLACK)

        ms = clock.tick()
        seconds = ms / 1000

        mouse_pos = pygame.mouse.get_pos()
        mouse_col = get_col_from_x(mouse_pos[0])
        if game_over:
            # Draw win text
            draw_text(
                screen, "You won!! Press R to restart", 32, 200, 50, (0, 255, 0))
        else:
            # Draw column mouse hovers over
            hover_mouse(screen, mouse_col, c.total_rows, c.turn)

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                move_success = c.make_move(mouse_col)
                if move_success:
                    landed_tile = len(c.board[mouse_col]) - 1
                    top_coords = get_tile_pos(mouse_col, c.total_rows)
                    tile_coords = get_tile_pos(mouse_col, landed_tile)
                    # Create animated piece
                    falling_pieces[(mouse_col, landed_tile)] = FallingPoint(
                        top_coords, 0, 1000, tile_coords[1])
                    # Check win
                    if c.check_win_at(mouse_col, landed_tile):
                        # Someone won
                        game_over = True
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    # Reset game
                    c.reset_game()
                    game_over = False

        update_all_falling(falling_pieces, seconds)
        draw_board(screen, c, falling_pieces)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
