import pygame
from classes.scene import Scene, SceneManager
from game_scene import GameScene
from classes.selector import IntSelector
from classes.text_box import TextBox
from classes.button import Button
from constants import BOARD_BOTTOM_LEFT, WHITE, BG_COLOR_MAIN_MENU, PLR_COLORS
from drawer import draw_text
from classes.player import Player


class MainMenu(Scene):
    col_buttons: IntSelector
    row_buttons: IntSelector
    player_number_buttons: IntSelector
    player_text_boxes: list[TextBox]
    play_button: Button

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.col_buttons = IntSelector(655, 200, 50, 50, 7, 2, 10)
        self.row_buttons = IntSelector(655, 300, 50, 50, 6, 2, 10)
        self.player_number_buttons = IntSelector(655, 400, 50, 50, 2, 2, 4)
        self.player_text_boxes = [TextBox(165 + i * 250, 500, 200, 50, f'PLAYER{i + 1}', 7) for i in range(4)]
        self.play_button = Button(540, 600, 200, 50, 'PLAY', self.play)
        self.scene_manager = None

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
        for event in events:
            self.col_buttons.update(event)
            self.row_buttons.update(event)
            self.player_number_buttons.update(event)
            # Only update the selected player
            for i in range(self.player_number_buttons.value):
                self.player_text_boxes[i].update(event)
            self.play_button.update(event)

    def draw(self):
        """Draws the scene to the screen
        """
        # Draw background
        self.screen.fill(BG_COLOR_MAIN_MENU)
        # Draw title
        draw_text(self.screen, 'Connect4', 100, 375, 25, WHITE)
        # Draw column buttons
        self.col_buttons.background_color = BG_COLOR_MAIN_MENU
        self.col_buttons.next_button.bg_color = BG_COLOR_MAIN_MENU
        self.col_buttons.previous_button.bg_color = BG_COLOR_MAIN_MENU
        self.col_buttons.next_button.border_color = BG_COLOR_MAIN_MENU
        self.col_buttons.previous_button.border_color = BG_COLOR_MAIN_MENU
        self.col_buttons.draw(self.screen)
        draw_text(self.screen, 'Columns: ', 40, 455, 200, WHITE)
        # Draw row buttons
        self.row_buttons.background_color = BG_COLOR_MAIN_MENU
        self.row_buttons.next_button.bg_color = BG_COLOR_MAIN_MENU
        self.row_buttons.previous_button.bg_color = BG_COLOR_MAIN_MENU
        self.row_buttons.next_button.border_color = BG_COLOR_MAIN_MENU
        self.row_buttons.previous_button.border_color = BG_COLOR_MAIN_MENU
        self.row_buttons.draw(self.screen)
        draw_text(self.screen, 'Rows: ', 40, 530, 300, WHITE)
        # Draw player number buttons
        self.player_number_buttons.background_color = BG_COLOR_MAIN_MENU
        self.player_number_buttons.next_button.bg_color = BG_COLOR_MAIN_MENU
        self.player_number_buttons.previous_button.bg_color = BG_COLOR_MAIN_MENU
        self.player_number_buttons.next_button.border_color = BG_COLOR_MAIN_MENU
        self.player_number_buttons.previous_button.border_color = BG_COLOR_MAIN_MENU
        self.player_number_buttons.draw(self.screen)
        draw_text(self.screen, 'Players: ', 40, 460, 400, WHITE)
        # Draw player text boxes
        for i in range(self.player_number_buttons.value):  # Only draw the number of players selected
            self.player_text_boxes[i].draw(self.screen)
        # Draw play button
        self.play_button.bg_color = BG_COLOR_MAIN_MENU
        self.play_button.text_color = WHITE
        self.play_button.border_color = BG_COLOR_MAIN_MENU
        self.play_button.draw(self.screen)

        pygame.display.update()
