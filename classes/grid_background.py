import pygame
from classes.falling_point import FallingPoint
from constants import PLR_COLORS, BG_COLOR_MAIN_MENU
import random


class GridBackground:
    screen: pygame.Surface
    falling_pieces: dict[int, FallingPoint]
    active_falling: bool
    surface: pygame.Surface
    amount_players: int

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.falling_pieces = {}
        self.active_falling = True
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.draw_grid()
        self.amount_players = 4

    def draw_grid(self):
        """Draws the grid of the board

        Returns: None

        """
        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        surface.fill(BG_COLOR_MAIN_MENU)

        width = 100
        height = 100
        screen_width = self.screen.get_size()[0]
        screen_height = self.screen.get_size()[1]
        amount_x = screen_width // width + 1
        amount_y = screen_height // height + 1
        x = screen_width / 2 - (amount_x * width) / 2
        y = screen_height / 2 - (amount_y * height) / 2

        for i in range(amount_x):
            pygame.draw.line(surface, (0, 0, 0, 0), (x + i * width, y), (x + i * width, screen_height), 1)
        for i in range(amount_y):
            pygame.draw.line(surface, (0, 0, 0, 0), (x, y + i * height), (screen_width, y + i * height), 1)
        self.surface = surface

    def draw(self):
        self.screen.fill((20, 20, 20))
        for key in self.falling_pieces:
            pygame.draw.circle(self.screen, PLR_COLORS[key], (self.falling_pieces[key].x, self.falling_pieces[key].y),
                               150)
        self.screen.blit(self.surface, (0, 0))

    def update(self, dt: float):

        if len(self.falling_pieces) < 1 and self.active_falling:
            self.falling_pieces[random.randint(0, self.amount_players - 1)] = FallingPoint(
                (random.randint(0, self.screen.get_width()), -150),
                650, 0,
                2 * self.screen.get_size()[1])

        keys_to_remove = []

        # Update all falling pieces
        for key in self.falling_pieces:
            self.falling_pieces[key].update(dt)
            if self.falling_pieces[key].is_past_max:
                keys_to_remove.append(key)

        # Remove pieces past max_y
        for key in keys_to_remove:
            del self.falling_pieces[key]
