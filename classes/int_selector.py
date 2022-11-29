import pygame
from classes.button import Button
from constants import FONT_PATH


class Selector:
    x: int
    y: int
    height: int
    button_width: int
    options: list
    current_index: int = 0
    value = property(lambda self: self.options[self.current_index])
    font: pygame.font.Font
    font_color: tuple[int, int, int]
    background_color: tuple[int, int, int]

    next_button: Button
    previous_button: Button

    def __init__(self, x: int, y: int, height: int, button_width: int, options: list):
        self.x = x
        self.y = y
        self.height = height
        self.button_width = button_width
        self.options = options

        self.font = pygame.font.Font(FONT_PATH, height)
        self.font_color = (255, 255, 255)
        self.background_color = (0, 0, 0)

        self.next_button = Button(
            x + button_width * 2, y, button_width, height, ">", self.next_option)
        self.previous_button = Button(
            x, y, button_width, height, "<", self.previous_option)

        self.next_button.text_color = self.font_color
        self.previous_button.text_color = self.font_color
        self.next_button.bg_color = self.background_color
        self.previous_button.bg_color = self.background_color

    def next_option(self):
        self.current_index = (self.current_index + 1) % len(self.options)

    def previous_option(self):
        self.current_index = (self.current_index - 1) % len(self.options)

    def draw(self, surface: pygame.Surface):
        # Draw the background
        pygame.draw.rect(surface, self.background_color, (self.x,
                                                          self.y, self.button_width * 3, self.height))
        # Draw the buttons
        self.next_button.draw(surface)
        self.previous_button.draw(surface)
        # Draw the value
        # value_text = self.font.render(str(self.value), True, self.font_color)
        # text_size = value_text.get_size()
        # surface.blit(value_text, (self.x + self.button_width *
        #                           1.5 - text_size[0] / 2, self.y + self.height / 2 - text_size[1] / 2))

    def update(self, event: pygame.event.Event):
        self.next_button.update(event)
        self.previous_button.update(event)


class IntSelector(Selector):

    def __init__(self, x: int, y: int, height: int, btn_width: int, default_value: int, min_value: int, max_value: int):
        nums = list(range(min_value, max_value + 1))
        super().__init__(x, y, height, btn_width, nums)
        self.current_index = nums.index(default_value)

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        # Draw the value
        value_text = self.font.render(str(self.value), True, self.font_color)
        text_size = value_text.get_size()
        surface.blit(value_text, (self.x + self.button_width *
                                  1.5 - text_size[0] / 2, self.y + self.height / 2 - text_size[1] / 2))


class ColorSelector(Selector):

    def __init__(self, x: int, y: int, height: int, btn_width: int, default_value: tuple[int, int, int], options: list):
        super().__init__(x, y, height, btn_width, options)
        self.current_index = options.index(default_value)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.value, (self.x + self.button_width, self.y,
                         self.button_width, self.height))
        # Draw the border
        pygame.draw.rect(surface, (255, 255, 255), (self.x + self.button_width, self.y,
                         self.button_width, self.height), 2)
        # Draw the buttons
        self.next_button.draw(surface)
        self.previous_button.draw(surface)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('IntSelector')
    s = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    int_selector = IntSelector(100, 100, 36, 36, 3, 0, 10)
    color_selector = ColorSelector(100, 200, 36, 36, (0, 0, 0), [(
        0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)])

    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            int_selector.update(e)
            color_selector.update(e)

        s.fill((0, 0, 0))
        int_selector.draw(s)
        color_selector.draw(s)
        pygame.display.update()
