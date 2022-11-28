import pygame
from classes.scene import Scene, SceneManager
from game_scene import GameScene
from classes.int_selector import IntSelector
from classes.text_box import TextBox
from classes.button import Button


class MainMenu(Scene):
    col_buttons: IntSelector
    row_buttons: IntSelector
    player_number_buttons: IntSelector
    player_text_boxes: list[TextBox]
    play_button: Button

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.col_buttons = IntSelector(100, 100, 50, 50, 3, 3, 10)
        self.row_buttons = IntSelector(100, 200, 50, 50, 3, 3, 10)
        self.player_number_buttons = IntSelector(100, 300, 50, 50, 2, 2, 4)
        self.player_text_boxes = [TextBox(100, 400 + i * 50, 200, 50, f'Player {i + 1}', 7) for i in range(4)]
        self.play_button = Button(100, 500, 200, 50, 'Play', self.play)

    def play(self):
        game_scene = GameScene(self.screen, (100, 600), self.col_buttons.value, self.row_buttons.value, [])
        self.scene_manager.add_scene(game_scene)

    def update(self, events: list[pygame.event.Event], seconds: float, scene_manager: SceneManager):
        self.scene_manager = scene_manager

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.play_button.draw(self.screen)
        pygame.display.update()
