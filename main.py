import pygame


pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen parameters
WIDTH = 900
HEIGHT = 600

# Create screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect4")

# Variables
TILE_SIZE = 20


def draw_grid(w: int, h: int):
    pass


def draw_board(board: list[list[int]]):
    pass


def main():
    while True:

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break


if __name__ == '__main__':
    main()
