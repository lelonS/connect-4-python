import pygame
from constants import FONT_PATH


def draw_text(screen: pygame.Surface, text: str, size: int, x: int, y: int, color: tuple):
    font = pygame.font.Font(FONT_PATH, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
