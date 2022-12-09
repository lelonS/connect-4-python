import pygame
from constants import BLACK
from classes.text_label import Label, CENTER

COLOR_INACTIVE = (185, 185, 185)
COLOR_ACTIVE = (105, 105, 105)
ERROR_COLOR = (200, 20, 20)


class TextBox:
    text: str
    rect: pygame.Rect
    text_color: tuple[int, int, int]
    bg_color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    border_width: int
    max_chars: int
    is_focused: bool
    default_text: str
    error: bool

    default_label: Label
    text_label: Label

    def __init__(self, x: int, y: int, width: int, height: int, default_text: str, max_chars: int):
        self.text = ""
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = BLACK
        self.bg_color = COLOR_INACTIVE
        self.border_color = BLACK
        self.border_width = 3
        self.max_chars = max_chars
        self.is_focused = False
        self.default_text = default_text
        self.error = False

        font_size = height - 10

        cx = self.rect.centerx
        cy = self.rect.centery
        default_text_color = (75, 75, 75)  # LightGray

        self.default_label = Label(self.default_text, font_size, cx, cy, default_text_color, CENTER)
        self.text_label = Label(self.text, font_size, cx, cy, self.text_color, CENTER)

    @property
    def value(self):
        """

        Returns: The text in the textbox or default text if the textbox is empty

        """
        if self.text == "":
            return self.default_text
        return self.text

    def draw(self, screen: pygame.Surface):
        """Draw the textbox on the screen

        Args:
            screen: The screen to draw on

        """
        # Draw background
        if self.error:
            pygame.draw.rect(screen, ERROR_COLOR, self.rect)
        elif self.is_focused:
            pygame.draw.rect(screen, COLOR_ACTIVE, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        # Draw text
        if self.text == "" and not self.is_focused:
            self.default_label.draw(screen, self.rect.centerx, self.rect.centery)
        else:
            if self.is_focused:
                self.text_label.set_text(">" + self.text + "<")
            else:
                self.text_label.set_text(self.text)
            self.text_label.draw(screen, self.rect.centerx, self.rect.centery)

    def update(self, event: pygame.event.Event):
        """Update the textbox based on the event

        Args:
            event: Events excluding QUIT

        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_focused = True
                # self.bg_color = COLOR_ACTIVE
            else:
                self.is_focused = False
                # self.bg_color = COLOR_INACTIVE
        if event.type == pygame.KEYDOWN and self.is_focused:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.is_focused = False
                # self.bg_color = COLOR_INACTIVE
            elif len(self.text) < self.max_chars:
                if event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    self.text += event.unicode.upper()
        self.text_label.set_text(self.text)
