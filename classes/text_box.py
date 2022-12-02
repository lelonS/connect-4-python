import pygame
from constants import FONT_PATH

COLOR_INACTIVE = (141, 182, 205)  # LightSkyBlue3
COLOR_ACTIVE = (28, 134, 238)  # DodgerBlue2


class TextBox:
    text: str
    rect: pygame.Rect
    text_color: tuple[int, int, int]
    bg_color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    border_width: int
    font: pygame.font.Font
    font_size: int
    max_chars: int
    is_focused: bool
    default_text: str
    default_text_color: tuple[int, int, int]

    def __init__(self, x: int, y: int, width: int, height: int, default_text: str, max_chars: int):
        self.text = ""
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = (0, 0, 0)
        self.bg_color = COLOR_INACTIVE
        self.border_color = (0, 0, 0)
        self.border_width = 2
        self.font_size = height - 10
        self.font = pygame.font.Font(FONT_PATH, self.font_size)
        self.max_chars = max_chars
        self.is_focused = False
        self.default_text = default_text
        self.default_text_color = (75, 75, 75)

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
        pygame.draw.rect(screen, self.bg_color, self.rect)
        # Draw border
        pygame.draw.rect(screen, self.border_color,
                         self.rect, self.border_width)
        # Draw text
        if self.text == "" and not self.is_focused:
            text = self.font.render(
                self.default_text, True, self.default_text_color)
        else:
            if self.is_focused:
                text = self.font.render(
                    ">" + self.text + "<", True, self.text_color)
            else:
                text = self.font.render(self.text, True, self.text_color)
        # screen.blit(text, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(text, text.get_rect(center=self.rect.center))

    def update(self, event: pygame.event.Event):
        """Update the textbox based on the event

        Args:
            event: Events excluding QUIT

        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_focused = True
                self.bg_color = COLOR_ACTIVE
            else:
                self.is_focused = False
                self.bg_color = COLOR_INACTIVE
        if event.type == pygame.KEYDOWN and self.is_focused:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.is_focused = False
                self.bg_color = COLOR_INACTIVE
            elif len(self.text) < self.max_chars:
                if event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    self.text += event.unicode.upper()


if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(500, 50)
    s = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("TextBox")

    text_boxes = [
        TextBox(100, 100, 200, 50, "PLAYER1", 7),
        TextBox(100, 200, 200, 50, "PLAYER2", 7),
        TextBox(100, 300, 200, 50, "PLAYER3", 7),
        TextBox(100, 400, 200, 50, "PLAYER4", 7)
    ]

    run = True
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            for textbox in text_boxes:
                textbox.update(e)
        s.fill((100, 100, 100))
        for textbox in text_boxes:
            textbox.draw(s)
        pygame.display.update()

    pygame.quit()
