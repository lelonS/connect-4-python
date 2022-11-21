import pygame
from classes.falling_point import FallingPoint
from classes.connect4 import ConnectFour
from classes.player import Player


class GameScreen:
    screen: pygame.Surface
    game: ConnectFour
    falling_pieces: dict[tuple, FallingPoint]

    tile_size: int
    board_bottom_left: tuple[int, int]
    players: list[Player]

    def __init__(self, screen: pygame.Surface, tile_size: int, board_bottom_left: tuple[int, int], plrs: list[Player]):
        self.screen = screen
        self.falling_pieces = {}
        self.tile_size = tile_size
        self.board_bottom_left = board_bottom_left
        self.players = plrs
