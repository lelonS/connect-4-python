import pygame
from classes.button import Button
from constants import GAME_FONT


class IntSelector:
    x: int
    y: int
    height: int
    button_width: int
    value: int
    min_value: int
    max_value: int
    font: pygame.font.Font
    font_color: tuple[int, int, int]
    background_color: tuple[int, int, int]

    increase_button: Button
    decrease_button: Button

    def __init__(self, x: int, y: int, height: int, btn_width: int, default_value: int, min_value: int, max_value: int):
        self.x = x
        self.y = y
        self.height = height
        self.button_width = btn_width
        self.value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.font = pygame.font.Font(GAME_FONT, height)
        self.font_color = (255, 255, 255)
        self.background_color = (0, 0, 0)

        self.decrease_button = Button(
            x, y, btn_width, height, '-', self.decrease)
        self.increase_button = Button(
            x + btn_width * 2, y, btn_width, height, '+', self.increase)

        self.decrease_button.bg_color = self.background_color
        self.increase_button.bg_color = self.background_color
        self.decrease_button.text_color = self.font_color
        self.increase_button.text_color = self.font_color

    def increase(self):
        if self.value < self.max_value:
            self.value += 1

    def decrease(self):
        if self.value > self.min_value:
            self.value -= 1

    def draw(self, surface: pygame.Surface):
        # Draw the background
        pygame.draw.rect(surface, self.background_color, (self.x,
                                                          self.y, self.button_width * 3, self.height))
        # Draw the buttons
        self.increase_button.draw(surface)
        self.decrease_button.draw(surface)
        # Draw the value
        value_text = self.font.render(str(self.value), True, self.font_color)
        text_size = value_text.get_size()
        surface.blit(value_text, (self.x + self.button_width *
                                  1.5 - text_size[0] / 2, self.y))

    def update(self, event: pygame.event.Event):
        self.increase_button.update(event)
        self.decrease_button.update(event)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('IntSelector')
    s = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    int_selector = IntSelector(100, 100, 36, 36, 3, 0, 10)

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            int_selector.update(e)

        s.fill((0, 0, 0))
        int_selector.draw(s)
        pygame.display.update()
