import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

cordinat: tuple[int, int] = pygame.mouse.get_pos()
print(cordinat)
