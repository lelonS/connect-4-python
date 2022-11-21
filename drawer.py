import pygame


def draw_text(screen: pygame.Surface, text: str, size: int, x: int, y: int, color: tuple):
    font = pygame.font.SysFont("consolas", size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
