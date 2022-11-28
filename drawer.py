import pygame
from constants import GAME_FONT


def draw_text(screen: pygame.Surface, text: str, size: int, x: int, y: int, color: tuple):
    font = pygame.font.Font(GAME_FONT, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
