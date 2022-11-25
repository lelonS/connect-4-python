import pygame
from constants import WIDTH, HEIGHT, BOARD_BOTTOM_LEFT
from game_screen import GameScreen
from classes.button import Button

pygame.init()

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect4")


def start_game():
    game_screen = GameScreen(screen, BOARD_BOTTOM_LEFT, 7, 6, [])
    game_screen.run_game()


def main():
    # Play button
    play_button = Button(325, 200, 250, 100, "PLAY", start_game)
    play_button.bg_color = (0, 0, 0)
    play_button.text_color = (255, 255, 255)

    # Main menu
    while True:
        # Draw background
        screen.fill((0, 0, 0))

        # Draw buttons
        play_button.draw(screen)

        # Update screen
        pygame.display.update()

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            play_button.update(event)

    # Open game screen
    # game_screen = GameScreen(screen, (0, 600), 7, 6, [])
    # game_screen.run_game()


if __name__ == '__main__':
    main()
