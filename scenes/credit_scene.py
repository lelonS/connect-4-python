import pygame
from classes.scene import Scene
from classes.text_label import Label, CENTER
from classes.button import Button
from constants import WHITE


class Credits(Scene):
    back_button: Button
    labels: list[list[float, Label]]

    def __init__(self, screen: pygame.Surface, scene_manager):
        super().__init__(screen, scene_manager)

        self.back_button = Button(40, screen.get_height() - 100, 100, 50, 'BACK', self.scene_manager.go_back)

        # Find best player
        best_player = None
        best_score = 0
        for player in self.scene_manager.highscores:
            if self.scene_manager.highscores[player]['wins'] > best_score:
                best_score = self.scene_manager.highscores[player]['wins']
                best_player = player
        credit_list = ['CREDITS', '', 'CONNECT 4', 'PVT 2022 - KYH', '', 'TEDDY - IndexError: list index out of range',
                       'LEON - NameError: name \'LEON\' is not defined',
                       'ALI - func() takes exactly 2 arguments (2 given)', 'JNTHN - print("Hello World!")',
                       '', 'BEST PLAYER', f'{best_player} - {best_score} WINS']

        self.labels = []

        for i, text in enumerate(credit_list):
            screen_r = screen.get_rect()
            font_size = 40
            if i >= 5:
                font_size = 30
            label = Label(text, font_size, screen_r.centerx, screen_r.bottom + i * 45, WHITE, CENTER)
            y_pos = screen_r.bottom + i * 45
            self.labels.append([y_pos, label])

    def draw(self):
        self.back_button.draw(self.screen)
        for pos_y, label in self.labels:
            label.draw(self.screen, y=int(pos_y))

        pygame.display.update()

    def update(self, events: list[pygame.event.Event], dt: float):
        for event in events:
            self.back_button.update(event)

        if self.labels[0][0] > 100:
            for i in range(len(self.labels)):
                self.labels[i][0] -= 120 * dt
