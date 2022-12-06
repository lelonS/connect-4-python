import pygame
from constants import WHITE
import classes.label as label
from classes.label import Label


class Button:
    text: Label
    hover_text: Label

    rect: pygame.Rect
    text_color: tuple[int, int, int]
    hover: bool
    on_click: callable

    def __init__(self, x: int, y: int, width: int, height: int, text: str, on_click: callable):
        font_size = int(height * 0.8)
        text_color = WHITE
        self.rect = pygame.Rect(x, y, width, height)
        cx = self.rect.centerx
        cy = self.rect.centery
        self.text = Label(text, font_size, cx, cy, text_color, align=label.CENTER)
        self.hover_text = Label(text, int(font_size * 1.2), cx, cy, text_color, align=label.CENTER)
        self.hover = False
        self.on_click = on_click

    def draw(self, screen: pygame.Surface):
        # draw text in center
        if self.hover:
            self.hover_text.draw(screen)
        else:
            self.text.draw(screen)

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
