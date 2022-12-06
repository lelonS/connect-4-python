import pygame
from constants import FONT_PATH


CENTER = 0
TOP_LEFT = 1
TOP_RIGHT = 2
TOP_CENTER = 3


class Label:
    _text: str
    _rendered_text: pygame.Surface
    _font: pygame.font.Font
    _font_size: int
    _font_color: tuple[int, int, int]

    x: int
    y: int
    align: int

    def __init__(self, text: str, font_size: int, x: int, y: int, color: tuple[int, int, int], align: int = 1):
        self._text = text
        self._font_size = font_size
        self._font_color = color
        self._font = pygame.font.Font(FONT_PATH, self._font_size)
        self.render_font()
        self.align = align
        self.x = x
        self.y = y

    def render_font(self):
        self._rendered_text = self._font.render(self._text, True, self._font_color)

    def set_text(self, text: str):
        # If text is same dont render again
        if self._text == text:
            return
        self._text = text
        self.render_font()

    def set_size(self, size: int):
        # If size is same dont render again
        if self._font_size == size:
            return
        self._font_size = size
        self._font = pygame.font.Font(FONT_PATH, self._font_size)
        self.render_font()

    def set_color(self, color: tuple[int, int, int]):
        # If size is same dont render again
        if self._font_color == color:
            return
        self._font_color = color
        self.render_font()

    def get_pos_aligned(self) -> tuple[int, int]:
        if self.align == CENTER:
            new_x = self.x - self._rendered_text.get_width() / 2
            new_y = self.y - self._rendered_text.get_height() / 2
        elif self.align == TOP_CENTER:
            new_x = self.x - self._rendered_text.get_width() / 2
            new_y = self.y
        elif self.align == TOP_LEFT:
            return self.x, self.y
        elif self.align == TOP_RIGHT:
            new_x = self.x - self._rendered_text.get_width()
            new_y = self.y
        else:
            return self.x, self.y
        return int(new_x), int(new_y)

    def get_size(self) -> tuple[int, int]:
        return self._rendered_text.get_size()

    def draw(self, screen: pygame.Surface):
        screen.blit(self._rendered_text, self.get_pos_aligned())
