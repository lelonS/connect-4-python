import pygame
from constants import WHITE
from classes.button import Button
from classes.text_label import Label, CENTER, TOP_CENTER


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

        self.next_button = Button(x + button_width * 2, y, button_width, height, ">", self.next_option)
        self.previous_button = Button(x, y, button_width, height, "<", self.previous_option)

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

    def draw(self, screen: pygame.Surface):
        """Draws the selector

        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Draw the buttons
        self.next_button.draw(screen)
        self.previous_button.draw(screen)

    def update(self, event: pygame.event.Event):
        """Updates the selector

        Args:
            event (pygame.event.Event): Current event
        """
        # Set last change to none and then update the buttons
        self.last_change = 0
        self.next_button.update(event)
        self.previous_button.update(event)


class IntSelector(Selector):

    label: Label

    def __init__(self, x: int, y: int, h: int, btn_width: int, default_val: int, min_val: int, max_val: int, **kwargs):
        nums = list(range(min_val, max_val + 1))
        super().__init__(x, y, h, btn_width, nums, **kwargs)
        self.value = default_val
        self.label = Label(str(self.value), h, int(x + btn_width * 1.5), int(y + h / 2), WHITE, CENTER)

    def update(self, event: pygame.event.Event):
        super().update(event)
        self.label.set_text(str(self.value))

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        # Draw the value
        self.label.draw(screen)


class ModeSelector(Selector):
    mode_label: Label
    description_label: Label

    def __init__(self, x: int, y: int, height: int, button_width: int, text_width, **kwargs):
        modes = [("Connect4", "Classic"), ("Blind4", "Every player is the same color")]
        super().__init__(x, y, height, button_width, modes, **kwargs)
        mid_x = x + (button_width * 2 + text_width) / 2
        self.mode_label = Label(self.value[0], height, mid_x, y + height // 2, WHITE, CENTER)
        self.description_label = Label(self.value[1], int(height * 0.2), mid_x, y + height, WHITE, TOP_CENTER)

        # Create a next button at the correct position
        self.next_button = Button(x + button_width + text_width, y, button_width, height, ">", self.next_option)

    def update(self, event: pygame.event.Event):
        super().update(event)
        self.mode_label.set_text(self.value[0])
        self.description_label.set_text(self.value[1])

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        # Draw the mode name
        self.mode_label.draw(screen)
        # Draw the description
        self.description_label.draw(screen)


# class SelectorGroup:
#     """A class that represents a group of selectors which can't have the same value
#     Attributes:
#         selectors (list[Selector]): List of selectors that can't have the same value
#     """
#     selectors: list[Selector]

#     def __init__(self, selectors: list[Selector], all_options: list = None):
#         self.selectors = selectors
#         for n, selector in enumerate(self.selectors):
#             if all_options is not None:
#                 selector.options = all_options
#             # Set last_change to 1 to change duplicated forwards the first selector doesn't change
#             if n != 0:
#                 selector.last_change = 1
#         self._change_duplicates()

#     def _change_duplicates(self):
#         # Get the last changed selectors
#         changed_selectors = [
#             selector for selector in self.selectors if selector.last_change != 0]
#         for selector in changed_selectors:
#             total_checks = 0  # Makes sure it doesn't get stuck in an infinite loop
#             # Current values taken by other selectors
#             current_values = [s.value for s in self.selectors if s != selector]
#             # Find a new value that is not taken
#             while selector.value in current_values and total_checks < len(selector.options):
#                 if selector.last_change == 1:
#                     selector.next_option()
#                 elif selector.last_change == -1:
#                     selector.previous_option()
#                 total_checks += 1

#     def draw(self, surface: pygame.Surface):
#         for selector in self.selectors:
#             selector.draw(surface)

#     def update(self, event: pygame.event.Event):
#         for selector in self.selectors:
#             selector.update(event)
#         self._change_duplicates()


# class ColorSelector(Selector):

#     def __init__(self, x: int, y: int, height: int, btn_width: int, options: list, **kwargs):
#         super().__init__(x, y, height, btn_width, options, **kwargs)
#         self._current_index = 0

#     def draw(self, surface: pygame.Surface):
#         pygame.draw.rect(surface, self.value, (self.x + self.button_width, self.y, self.button_width, self.height))
#         # Draw the border
#         pygame.draw.rect(surface, self.font_color, (self.x + self.button_width, self.y, self.button_width,
#         self.height), 2)
#         # Draw the buttons
#         self.next_button.draw(surface)
#         self.previous_button.draw(surface)
