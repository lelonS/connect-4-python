import pygame
from constants import WIDTH, HEIGHT, BLACK, PLR_COLORS
from classes.falling_point import FallingPoint
from classes.connect4 import ConnectFour
from drawer import draw_board, get_col_from_x, draw_text, get_tile_pos, hover_mouse


def update_all_falling(falling_pieces: dict[tuple, FallingPoint], dt: float):
    # Pieces past max_y to remove
    keys_to_remove = []

    # Update all falling pieces
    for key in falling_pieces:
        falling_pieces[key].update(dt)
        if falling_pieces[key].is_past_max:
            keys_to_remove.append(key)

    # Remove pieces past max_y
    for key in keys_to_remove:
        del falling_pieces[key]


def check_all_past(falling_pieces: dict, past_y: float) -> bool:
    # Check if all falling pieces are past a y value
    for piece in falling_pieces.values():
        if piece.y <= past_y:
            return False
    return True


def main():
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    c = ConnectFour(7, 6)  # 7, 6
    game_over = False

    # Dictionary (col, row):FallingPoint
    falling_pieces: dict[tuple, FallingPoint] = {}
    clock = pygame.time.Clock()
    winner = None

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

        # Check if all past or in top row
        can_move = check_all_past(
            falling_pieces, get_tile_pos(0, c.total_rows - 1)[1])

        if game_over:
            if winner is not None:
                # Draw win text
                draw_text(
                    screen, f"Player {winner} won!! Press R to restart", 32, 200, 50, PLR_COLORS[winner])
            else:
                # Draw tie text
                draw_text(screen, "Tie.. Press R to restart",
                          32, 200, 50, (125, 125, 125))

        elif can_move:
            # Draw column mouse hovers over if user can move
            hover_mouse(screen, mouse_col, c.total_rows, c.turn)

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and can_move:
                move_success = c.make_move(mouse_col)
                if move_success:
                    landed_row = len(c.board[mouse_col]) - 1
                    top_pos = get_tile_pos(mouse_col, c.total_rows)
                    landed_pos = get_tile_pos(mouse_col, landed_row)

                    # Create animated piece and add to dictionary
                    falling_pieces[(mouse_col, landed_row)] = FallingPoint(
                        top_pos, 0, 2300, landed_pos[1])

                    # Check win
                    if c.check_win_at(mouse_col, landed_row):
                        # Someone won
                        game_over = True
                        winner = c.board[mouse_col][landed_row]
                    elif c.check_board_full():
                        # Board full, and no winner = tue
                        game_over = True
                        winner = None
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    # Reset game
                    c.reset_game()
                    game_over = False
                    winner = None

        update_all_falling(falling_pieces, seconds)
        draw_board(screen, c, falling_pieces)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
