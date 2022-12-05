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
        self.falling_pieces = {}

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

    def draw_grid(self):
        """Draws the grid of the board

        Returns: None

        """
        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        surface.fill(BG_COLOR_MAIN_MENU)

        width = 100
        height = 100
        screen_width = self.screen.get_size()[0]
        screen_height = self.screen.get_size()[1]
        amount_x = screen_width // width + 1
        amount_y = screen_height // height + 1
        x = screen_width / 2 - (amount_x * width) / 2
        y = screen_height / 2 - (amount_y * height) / 2

        for i in range(amount_x):
            pygame.draw.line(surface, (0, 0, 0, 0), (x + i * width, y), (x + i * width, screen_height), 1)
        for i in range(amount_y):
            pygame.draw.line(surface, (0, 0, 0, 0), (x, y + i * height), (screen_width, y + i * height), 1)
        self.screen.blit(surface, (0, 0))

    def update_all_falling(self, dt: float):
        """Updates all falling pieces

        Args:
            dt (float): Seconds since last update
        """
        # Pieces past max_y to remove
        keys_to_remove = []

        # Update all falling pieces
        for key in self.falling_pieces:
            self.falling_pieces[key].update(dt)
            if self.falling_pieces[key].is_past_max:
                keys_to_remove.append(key)

        # Remove pieces past max_y
        for key in keys_to_remove:
            del self.falling_pieces[key]

    def draw_all_falling(self):
        """Draws all falling pieces

        Returns: None

        """
        for key in self.falling_pieces:
            pygame.draw.circle(self.screen, PLR_COLORS[key], (self.falling_pieces[key].x, self.falling_pieces[key].y),
                               150)

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
        self.check_duplicate_names()
        self.update_all_falling(seconds)

        if len(self.falling_pieces) < 1:
            self.falling_pieces[random.randint(0, self.player_number_buttons.value - 1)] = FallingPoint(
                (random.randint(0, self.screen.get_width()), -150),
                650, 0,
                2 * self.screen.get_size()[1])

    def draw(self):
        """Draws the scene to the screen
        """

        # Draw background
        self.screen.fill((20, 20, 20))
        # Draw falling pieces
        self.draw_all_falling()
        # draw a circle at mouse position
        # pygame.draw.circle(self.screen, (255, 0, 0), pygame.mouse.get_pos(), 70)

        # Draw background-grid
        self.draw_grid()
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
