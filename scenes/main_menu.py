import pygame
from classes.scene import Scene, SceneManager
from scenes.game_scene import GameScene
from classes.selector import IntSelector
from classes.text_box import TextBox
from classes.button import Button
from constants import BOARD_BOTTOM_LEFT, WHITE, BG_COLOR_MAIN_MENU, PLR_COLORS, BOARD_COLOR, BANANA
from drawer import draw_text
from classes.player import Player
from classes.falling_point import FallingPoint
import random


class MainMenu(Scene):
    col_buttons: IntSelector
    row_buttons: IntSelector
    player_number_buttons: IntSelector
    player_text_boxes: list[TextBox]
    play_button: Button

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        mid_x = int(screen.get_size()[0] / 2)
        px, py, pw, ph = self.get_rect(350, 175, 'top-center', (mid_x, 575))

        self.col_buttons = IntSelector(mid_x, 200, 50, 50, 7, 5, 12, background_color=BG_COLOR_MAIN_MENU)
        self.row_buttons = IntSelector(mid_x, 300, 50, 50, 6, 5, 12, background_color=BG_COLOR_MAIN_MENU)
        self.player_number_buttons = IntSelector(mid_x, 400, 50, 50, 2, 2, 4, background_color=BG_COLOR_MAIN_MENU)
        self.player_text_boxes = [TextBox(165 + i * 250, 500, 200, 50, f'PLAYER{i + 1}', 7) for i in range(4)]
        for i in range(4):  # TODO fix this
            self.player_text_boxes[i].border_color = PLR_COLORS[i]
        self.play_button = Button(px, py, pw, ph, 'PLAY', self.play)
        self.scene_manager = None

    @staticmethod
    def get_rect(width: int, height: int, align: str, pos: tuple[int, int]) -> tuple[int, int, int, int]:
        """

        Args:
            width: The width
            height: The height
            align: String of value(center, top-left, top-right)
            pos: Position to align to

        Returns: Rectangle with the new position

        """
        x = pos[0]
        y = pos[1]
        if align == 'center':
            new_x = x - width / 2
            new_y = y - height / 2
        elif align == 'top-center':
            new_x = x - width / 2
            new_y = y
        elif align == 'top-left':
            return pos[0], pos[1], width, height
        elif align == 'top-right':
            new_x = x - width
            new_y = y
        else:
            return pos[0], pos[1], width, height
        return int(new_x), int(new_y), width, height

    def check_duplicate_names(self):
        all_names = []
        for i in range(self.player_number_buttons.value):
            all_names.append(self.player_text_boxes[i].value)

        for i in range(self.player_number_buttons.value):
            textbox = self.player_text_boxes[i]
            if all_names.count(textbox.value) > 1:
                textbox.error = True
            else:
                textbox.error = False

    def play(self):
        """Starts the game with the selected settings

        Returns: None

        """
        players = []
        selected_names = []
        for i in range(self.player_number_buttons.value):
            name = self.player_text_boxes[i].value
            if name in selected_names:
                return
            selected_names.append(name)
            new_player = Player(name, PLR_COLORS[i])
            players.append(new_player)

        game_scene = GameScene(self.screen, BOARD_BOTTOM_LEFT, self.col_buttons.value, self.row_buttons.value, players)
        self.scene_manager.add_scene(game_scene)

    def update(self, events: list[pygame.event.Event], seconds: float, scene_manager: SceneManager):
        """Updates the scene and handles events

        Args:
            events: A list of pygame events
            seconds: The number of seconds since the last update
            scene_manager: The scene manager that is managing this scene

        Returns:

        """
        self.scene_manager = scene_manager
        self.scene_manager.grid_background.active_falling = True
        self.scene_manager.grid_background.amount_players = self.player_number_buttons.value
        for event in events:
            self.col_buttons.update(event)
            self.row_buttons.update(event)
            self.player_number_buttons.update(event)
            # Only update the selected player
            for i in range(self.player_number_buttons.value):
                self.player_text_boxes[i].update(event)
            self.play_button.update(event)
        self.check_duplicate_names()

    def draw(self):
        """Draws the scene to the screen
        """

        # draw a circle at mouse position
        # pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 70)
        # Draw title
        draw_text(self.screen, 'Connect4', 100, 375, 25, WHITE)
        # Draw column buttons
        self.col_buttons.draw(self.screen)
        draw_text(self.screen, 'Columns: ', 40, 445, 200, WHITE)
        # Draw row buttons
        self.row_buttons.draw(self.screen)
        draw_text(self.screen, 'Rows: ', 40, 518, 300, WHITE)
        # Draw player number buttons
        self.player_number_buttons.draw(self.screen)
        draw_text(self.screen, 'Players: ', 40, 446, 400, WHITE)
        # Draw player text boxes
        for i in range(self.player_number_buttons.value):  # Only draw the number of players selected
            self.player_text_boxes[i].draw(self.screen)
        # Draw play button
        self.play_button.bg_color = BG_COLOR_MAIN_MENU
        self.play_button.text_color = WHITE
        self.play_button.border_color = BG_COLOR_MAIN_MENU
        self.play_button.draw(self.screen)

        pygame.display.update()
