import pygame
from constants import FONT_PATH, BLACK


class Button:
    text: str
    rect: pygame.Rect
    text_color: tuple[int, int, int]
    font: pygame.font.Font
    hover_font: pygame.font.Font
    font_size: int
    hover: bool
    on_click: callable

    def __init__(self, x: int, y: int, width: int, height: int, text: str, on_click: callable):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = BLACK
        self.font_size = int(height * 0.8)
        self.font = pygame.font.Font(FONT_PATH, self.font_size)
        self.hover_font = pygame.font.Font(
            FONT_PATH, int(self.font_size * 1.2))
        self.hover = False
        self.on_click = on_click

    def draw(self, screen: pygame.Surface):
        # draw text in center
        if self.hover:
            text = self.hover_font.render(self.text, True, self.text_color)
        else:
            text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def update(self, event):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.hover = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_click()
        else:
            self.hover = False

# if __name__ == '__main__':
#     pygame.init()
#     s = pygame.display.set_mode((500, 500))
#     pygame.display.set_caption("Button")
#
#     button = Button(50, 50, 200, 60, 'test', lambda: print('clicked'))
#
#     run = True
#
#     while run:
#         for e in pygame.event.get():
#             button.update(e)
#             if e.type == pygame.QUIT:
#                 run = False
#
#         s.fill((0, 0, 0))
#         button.draw(s)
#         pygame.display.update()
#
#     pygame.quit()
