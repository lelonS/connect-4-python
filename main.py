import pygame
from constants import WIDTH, HEIGHT
from game_screen import GameScreen


def main():
    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    # Open game screen
    game_screen = GameScreen(screen, (0, 600), [])
    game_screen.run_game()


if __name__ == '__main__':
    main()
