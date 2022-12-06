import pygame
from classes.button import Button
from constants import FONT_PATH


# from constants import PLR_COLORS


class Selector:
    """A class that represent a selector for a list of options

    Attributes:
        x (int): x position
        y (int): y position
        height (int): height of the selector
        button_width (int): width of the 'next' and 'previous' buttons
        options (list): List of options
        last_change (int): 1 if the last change was to the next option,
                          -1 if the last change was to the previous option, 0 if there was no change

        font_color (tuple[int, int, int]): Color of the text

        next_button (Button): Button to change to the next option
        previous_button (Button): Button to change to the previous option
    """
    x: int
    y: int
    height: int
    button_width: int
    options: list
    _current_index: int = 0
    last_change: int  # -1 is previous, 1 is next, 0 is none

    font: pygame.font.Font
    font_color: tuple[int, int, int]

    next_button: Button
    previous_button: Button

    def __init__(self, x: int, y: int, height: int, button_width: int, options: list, **kwargs):
        self.x = x
        self.y = y
        self.height = height
        self.button_width = button_width
        self.options = options
        self._current_index = 0
        self.last_change = 0

        self.font = pygame.font.Font(FONT_PATH, height)
        self.font_color = kwargs.get("font_color", (255, 255, 255))

        self.next_button = Button(
            x + button_width * 2, y, button_width, height, ">", self.next_option)
        self.previous_button = Button(
            x, y, button_width, height, "<", self.previous_option)

        self.next_button.text_color = self.font_color
        self.previous_button.text_color = self.font_color

    def next_option(self):
        """Change the current option to the next one
        """
        self._current_index = (self._current_index + 1) % len(self.options)
        self.last_change = 1

    def previous_option(self):
        """Change the current option to the previous one
        """
        self._current_index = (self._current_index - 1) % len(self.options)
        self.last_change = -1

    @property
    def value(self):
        """The currently selected option

        Returns:
            _type_: The value of the currently selected option
        """
        return self.options[self._current_index]

    @value.setter
    def value(self, new_value):
        if new_value in self.options:
            self._current_index = self.options.index(new_value)

    def draw(self, surface: pygame.Surface):
        """Draws the selector

        Args:
            surface (pygame.Surface): The surface to draw on
        """
        # Draw the buttons
        self.next_button.draw(surface)
        self.previous_button.draw(surface)

    def update(self, event: pygame.event.Event):
        """Updates the selector

        Args:
            event (pygame.event.Event): Current event
        """
        # Set last change to none and then update the buttons
        self.last_change = 0
        self.next_button.update(event)
        self.previous_button.update(event)


class SelectorGroup:
    """A class that represents a group of selectors which can't have the same value
    Attributes:
        selectors (list[Selector]): List of selectors that can't have the same value
    """
    selectors: list[Selector]

    def __init__(self, selectors: list[Selector], all_options: list = None):
        self.selectors = selectors
        for n, selector in enumerate(self.selectors):
            if all_options is not None:
                selector.options = all_options
            # Set last_change to 1 to change duplicated forwards the first selector doesn't change
            if n != 0:
                selector.last_change = 1
        self._change_duplicates()

    def _change_duplicates(self):
        # Get the last changed selectors
        changed_selectors = [
            selector for selector in self.selectors if selector.last_change != 0]
        for selector in changed_selectors:
            total_checks = 0  # Makes sure it doesn't get stuck in an infinite loop
            # Current values taken by other selectors
            current_values = [s.value for s in self.selectors if s != selector]
            # Find a new value that is not taken
            while selector.value in current_values and total_checks < len(selector.options):
                if selector.last_change == 1:
                    selector.next_option()
                elif selector.last_change == -1:
                    selector.previous_option()
                total_checks += 1

    def draw(self, surface: pygame.Surface):
        for selector in self.selectors:
            selector.draw(surface)

    def update(self, event: pygame.event.Event):
        for selector in self.selectors:
            selector.update(event)
        self._change_duplicates()


class IntSelector(Selector):

    def __init__(self, x: int, y: int, h: int, btn_width: int, default_val: int, min_val: int, max_val: int, **kwargs):
        nums = list(range(min_val, max_val + 1))
        super().__init__(x, y, h, btn_width, nums, **kwargs)
        self.value = default_val

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        # Draw the value
        value_text = self.font.render(str(self.value), True, self.font_color)
        text_size = value_text.get_size()
        surface.blit(value_text, (self.x + self.button_width *
                                  1.5 - text_size[0] / 2, self.y + self.height / 2 - text_size[1] / 2))


class ColorSelector(Selector):

    def __init__(self, x: int, y: int, height: int, btn_width: int, options: list, **kwargs):
        super().__init__(x, y, height, btn_width, options, **kwargs)
        self._current_index = 0

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.value, (self.x + self.button_width, self.y,
                                               self.button_width, self.height))
        # Draw the border
        pygame.draw.rect(surface, self.font_color, (self.x + self.button_width, self.y,
                                                    self.button_width, self.height), 2)
        # Draw the buttons
        self.next_button.draw(surface)
        self.previous_button.draw(surface)

# if __name__ == "__main__":
#     pygame.init()
#     pygame.display.set_caption('IntSelector')
#     s = pygame.display.set_mode((800, 600))
#     clock = pygame.time.Clock()
#
#     int_selector = IntSelector(100, 100, 36, 36, 24321, 0, 50)
#     int_selector2 = IntSelector(200, 100, 36, 36, 7, 0, 10)
#     selector_group2 = SelectorGroup([int_selector, int_selector2])
#     color_selector = ColorSelector(100, 200, 36, 36, [])
#     color_selector2 = ColorSelector(100, 300, 36, 36, [])
#     color_selector3 = ColorSelector(100, 400, 36, 36, [])
#     selector_group = SelectorGroup(
#         [color_selector, color_selector2, color_selector3], PLR_COLORS)
#
#     while True:
#         clock.tick(60)
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             selector_group2.update(e)
#             selector_group.update(e)
#
#         s.fill((0, 0, 0))
#         selector_group2.draw(s)
#         selector_group.draw(s)
#         pygame.display.update()
