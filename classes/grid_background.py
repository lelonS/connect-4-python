import pygame
from classes.falling_point import FallingPoint
from constants import PLR_COLORS, BG_COLOR, GRID_COLOR, BLIND_COLOR
import random


class GridBackground:
    screen: pygame.Surface
    falling_pieces: list[tuple[int, FallingPoint]]
    active_falling: bool
    surface: pygame.Surface
    amount_players: int
    current_plr: int
    use_blind: bool

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.falling_pieces = []
        self.active_falling = True
        self.surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.draw_grid()
        self.amount_players = 4
        self.current_plr = 0
        self.use_blind = False

    def draw_grid(self):
        """Draws the grid of the board

        Returns: None

        """
        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        surface.fill(BG_COLOR)

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
        self.screen.fill(GRID_COLOR)
        circle_radius = 150
        for plr, piece in self.falling_pieces:
            if self.use_blind:
                pygame.draw.circle(self.screen, BLIND_COLOR, (piece.x, piece.y), circle_radius)
            else:
                pygame.draw.circle(self.screen, PLR_COLORS[plr], (piece.x, piece.y), circle_radius)
        self.screen.blit(self.surface, (0, 0))

    def update(self, dt: float):

        if len(self.falling_pieces) < 1 and self.active_falling:
            plr_num = self.current_plr  # random.randint(0, self.amount_players - 1)
            random_x = random.randint(0, self.screen.get_width())
            start_y = -150
            fall_speed = 650
            acc_y = 0
            max_y = 2 * self.screen.get_size()[1]
            self.falling_pieces.append((plr_num, FallingPoint((random_x, start_y), fall_speed, acc_y, max_y)))

            self.current_plr = (self.current_plr + 1) % self.amount_players

        pieces_to_remove = []
        # Update all falling pieces
        for plr, piece in self.falling_pieces:
            piece.update(dt)
            if piece.is_past_max:
                pieces_to_remove.append((plr, piece))

        # Remove pieces past max_y
        for val in pieces_to_remove:
            self.falling_pieces.remove(val)
