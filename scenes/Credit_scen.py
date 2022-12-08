import pygame
from pygame.locals import *
from classes.scene import Scene
from classes.text_box import TextBox
from classes.text_label import Label, CENTER, TOP_CENTER
from classes.button import Button
from constants import BG_COLOR, WHITE


class Credits(Scene):
    Credits_text_boxes: list[TextBox]

    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)

        self.back_button = Button(40, screen.get_height() - 200, 100, 50, 'BACK', self.scene_manager.go_back)

        credit_list = ['CREDITS', '', 'CONNECT 4', 'PVT 2022 - KYH', '', 'TEDDY - captain crunchtime',
                       'LEON - the sniper',
                       'ALI - the chief', 'JONATHAN - mr.late']

        self.texts = []

        for i, line in enumerate(credit_list):
            screen_r = screen.get_rect()
            s = Label(line, 40, screen_r.centerx, screen_r.bottom + i * 45, WHITE, CENTER)
            r = pygame.Rect(screen_r.centerx, screen_r.bottom + i * 45, 1, 1)
            self.texts.append((r, s))

    def draw(self):
        self.back_button.draw(self.screen)
        for r, s in self.texts:
            s.draw(self.screen, r.x, r.y)

        pygame.display.update()

    def update(self, events: list[pygame.event.Event], dt: float):
        for event in events:
            self.back_button.update(event)
        if self.texts[0][0].y > 100:
            for r, s in self.texts:
                r.move_ip(0, -1)
