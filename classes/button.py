import pygame
from constants import WHITE
from classes.text_label import Label, CENTER


class Button:
    text_label: Label
    hover_label: Label

    rect: pygame.Rect
    text_color: tuple[int, int, int]
    hover: bool
    on_click: callable
    load_sound: pygame.mixer.Sound

    def __init__(self, x: int, y: int, width: int, height: int, text: str, on_click: callable):
        font_size = height
        text_color = WHITE
        self.rect = pygame.Rect(x, y, width, height)
        cx = self.rect.centerx
        cy = self.rect.centery
        self.text_label = Label(text, font_size, cx, cy, text_color, align=CENTER)
        self.hover_label = Label(text, int(font_size * 1.2), cx, cy, text_color, align=CENTER)
        self.hover = False
        self.on_click = on_click
        self.load_sound = pygame.mixer.Sound("assets/sounds/click.ogg")

    def draw(self, screen: pygame.Surface):
        # draw text in center
        if self.hover:
            self.hover_label.draw(screen)
        else:
            self.text_label.draw(screen)

    def update(self, event):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.hover = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.on_click()
                self.load_sound.play()
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
