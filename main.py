import pygame


pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen parameters
WIDTH = 900
HEIGHT = 600


# Variables
TILE_SIZE = 20


def draw_grid(w: int, h: int):
    pass


def draw_pieces(board: list[list[int]]):
    pass


def main():

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect4")

    # Loop
    running = True
    while running:

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False


if __name__ == '__main__':
    main()
