import pygame


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
        self.bg_color = (255, 255, 255)
        self.border_color = (0, 0, 0)
        self.border_width = 2
        self.font_size = height
        self.font = pygame.font.SysFont("consolas", self.font_size)
        self.max_chars = max_chars
        self.is_focused = False
        self.default_text = default_text
        self.default_text_color = (150, 150, 150)

    def draw(self, screen: pygame.Surface):
        # Draw background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        # Draw text
        if self.text == "":
            text = self.font.render(self.default_text, True, self.default_text_color)
        else:
            text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("TextBox")

    text_box = TextBox(100, 100, 200, 50, "PLAYER1", 15)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.fill((0, 0, 0))
        text_box.draw(screen)
        pygame.display.update()

    pygame.quit()
