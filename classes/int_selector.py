import pygame


class IntSelector:
    x: int
    y: int
    height: int
    button_width: int
    value: int
    min_value: int
    max_value: int
    font: pygame.font.Font
    font_color: pygame.Color
    background_color: pygame.Color

    increase_button = None
    decrease_button = None

    def __init__(self, x: int, y: int, height: int, button_width: int, default_value: int, min_value: int, max_value: int):
        self.x = x
        self.y = y
        self.height = height
        self.button_width = button_width
        self.value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.font = pygame.font.SysFont('consolas', height)
        self.font_color = pygame.Color('white')
        self.background_color = pygame.Color('black')

    def draw(self, surface: pygame.Surface):
        # Draw the background
        pygame.draw.rect(surface, self.background_color, (self.x,
                         self.y, self.button_width * 3, self.height))
        # Draw the buttons
        # self.increase_button.draw(surface)
        # self.decrease_button.draw(surface)
        # Draw the value
        value_text = self.font.render(str(self.value), True, self.font_color)
        text_size = value_text.get_size()
        surface.blit(value_text, (self.x + self.button_width +
                     text_size[0] / 2, self.y))
